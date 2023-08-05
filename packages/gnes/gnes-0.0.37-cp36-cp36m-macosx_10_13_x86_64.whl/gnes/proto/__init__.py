#  Tencent is pleased to support the open source community by making GNES available.
#
#  Copyright (C) 2019 THL A29 Limited, a Tencent company. All rights reserved.
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import ctypes
import random
from typing import List
from typing import Optional

import numpy as np
import zmq
from termcolor import colored

from . import gnes_pb2
from ..helper import batch_iterator

__all__ = ['RequestGenerator', 'send_message', 'recv_message', 'blob2array', 'array2blob', 'gnes_pb2', 'add_route']


class RequestGenerator:
    @staticmethod
    def index(data: List[bytes], batch_size: int = 0, doc_type: int = gnes_pb2.Document.TEXT,
              doc_id_start: int = 0, request_id_start: int = 0,
              random_doc_id: bool = False,
              *args, **kwargs):

        for pi in batch_iterator(data, batch_size):
            req = gnes_pb2.Request()
            req.request_id = request_id_start
            for raw_bytes in pi:
                d = req.index.docs.add()
                d.doc_id = doc_id_start if not random_doc_id else random.randint(0, ctypes.c_uint(-1).value)
                d.raw_bytes = raw_bytes
                d.weight = 1.0
                d.doc_type = doc_type
                doc_id_start += 1
            yield req
            request_id_start += 1

    @staticmethod
    def train(data: List[bytes], batch_size: int = 0, doc_type: int = gnes_pb2.Document.TEXT,
              doc_id_start: int = 0, request_id_start: int = 0,
              random_doc_id: bool = False,
              *args, **kwargs):
        for pi in batch_iterator(data, batch_size):
            req = gnes_pb2.Request()
            req.request_id = request_id_start
            for raw_bytes in pi:
                d = req.train.docs.add()
                d.doc_id = doc_id_start if not random_doc_id else random.randint(0, ctypes.c_uint(-1).value)
                d.raw_bytes = raw_bytes
                d.doc_type = doc_type
                if not random_doc_id:
                    doc_id_start += 1
            yield req
            request_id_start += 1
        req = gnes_pb2.Request()
        req.request_id = request_id_start
        req.train.flush = True
        yield req
        request_id_start += 1

    @staticmethod
    def query(query: bytes, top_k: int, request_id_start: int = 0, doc_type: int = gnes_pb2.Document.TEXT, *args,
              **kwargs):
        if top_k <= 0:
            raise ValueError('"top_k: %d" is not a valid number' % top_k)

        req = gnes_pb2.Request()
        req.request_id = request_id_start
        req.search.query.raw_bytes = query
        req.search.query.doc_type = doc_type
        req.search.top_k = top_k
        yield req


def blob2array(blob: 'gnes_pb2.NdArray') -> np.ndarray:
    """
    Convert a blob proto to an array.
    """
    return np.frombuffer(blob.data, dtype=blob.dtype).reshape(blob.shape)


def array2blob(x: np.ndarray) -> 'gnes_pb2.NdArray':
    """Converts a N-dimensional array to blob proto.
    """
    blob = gnes_pb2.NdArray()
    blob.data = x.tobytes()
    blob.shape.extend(list(x.shape))
    blob.dtype = x.dtype.name
    return blob


def router2str(m: 'gnes_pb2.Message') -> str:
    return colored('▸', 'green').join([r.service for r in m.envelope.routes])


def add_route(evlp: 'gnes_pb2.Envelope', name: str):
    r = evlp.routes.add()
    r.service = name
    r.timestamp.GetCurrentTime()


def merge_routes(msg: 'gnes_pb2.Message', prev_msgs: List['gnes_pb2.Message'], idx: int = -1):
    msg.envelope.routes.extend([m.envelope.routes[idx] for m in prev_msgs[:-1]])


def send_message(sock: 'zmq.Socket', msg: 'gnes_pb2.Message', timeout: int = -1) -> None:
    try:
        if timeout > 0:
            sock.setsockopt(zmq.SNDTIMEO, timeout)
        else:
            sock.setsockopt(zmq.SNDTIMEO, -1)

        sock.send_multipart([msg.envelope.client_id.encode(), msg.SerializeToString()])
    except zmq.error.Again:
        raise TimeoutError(
            'cannot send message to sock %s after timeout=%dms, please check the following:'
            'is the server still online? is the network broken? are "port" correct? ' % (
                sock, timeout))
    finally:
        sock.setsockopt(zmq.SNDTIMEO, -1)


def recv_message(sock: 'zmq.Socket', timeout: int = -1) -> Optional['gnes_pb2.Message']:
    response = []
    try:
        if timeout > 0:
            sock.setsockopt(zmq.RCVTIMEO, timeout)
        else:
            sock.setsockopt(zmq.RCVTIMEO, -1)

        _, msg_data = sock.recv_multipart()
        msg = gnes_pb2.Message()
        msg.ParseFromString(msg_data)
        return msg

    except ValueError:
        raise ValueError('received a wrongly-formatted request (expected 4 frames, got %d)' % len(response))
    except zmq.error.Again:
        raise TimeoutError(
            'no response from sock %s after timeout=%dms, please check the following:'
            'is the server still online? is the network broken? are "port" correct? ' % (
                sock, timeout))
    finally:
        sock.setsockopt(zmq.RCVTIMEO, -1)
