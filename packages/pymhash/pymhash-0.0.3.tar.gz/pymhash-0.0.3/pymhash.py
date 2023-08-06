#!/usr/bin/env python
from ctypes import CDLL, c_char_p, c_int, c_void_p, c_ulonglong
from os import read, write
import eventlet
# import gevent
# from gevent.socket import wait_read

_lib = CDLL('libhasher.so')
_lib.hasher_create.restype = c_void_p
_lib.hasher_destroy.argtypes = (c_void_p,)

_lib.hasher_getfd.argtypes = (c_void_p,)
_lib.hasher_getfd.restype = c_int

_lib.hasher_queue_status.argtypes = (c_void_p,)
_lib.hasher_queue_status.restype = c_int

_lib.hasher_update.argtypes = (c_void_p, c_char_p, c_int)

_lib.hasher_result.argtypes = (c_void_p,)
_lib.hasher_result.restype = c_char_p


class BackgroundTask:
    def __init__(self):
        self.ctx = _lib.hasher_create()
        self.fd = _lib.hasher_getfd(self.ctx)
    def update(self, buf):
        if _lib.hasher_queue_status(self.ctx):
            eventlet.hubs.trampoline(self.fd, read=True)
        read(self.fd, 8)
        _lib.hasher_update(self.ctx, buf.encode('utf-8'), len(buf))
    def result(self):
        return _lib.hasher_result(self.ctx)
    def __del__(self):
        _lib.hasher_destroy(self.ctx)
