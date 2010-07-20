# -*- coding: utf-8 -*-
from threading import Thread
from Queue import Queue
import time
import unittest
import uuid

import libuuid


def test_property():
    _PROPERTIES = [
        'bytes', 'bytes_le', 'clock_seq', 'clock_seq_hi_variant',
        'clock_seq_low', 'fields', 'hex', 'node', 'time', 'time_hi_version',
        'time_low', 'time_mid', 'urn', 'variant', 'version']
    def _check_property(func_name, prop):
        u = getattr(libuuid, func_name)()
        c = uuid.UUID(bytes=u.bytes)
        assert getattr(u, prop) == getattr(c, prop)
    for prop in _PROPERTIES:
        yield _check_property, 'uuid1', prop
        yield _check_property, 'uuid4', prop


def test_method():
    _METHODS = [
        '__hash__', '__int__', '__repr__', '__str__', 'get_bytes',
        'get_bytes_le', 'get_clock_seq', 'get_clock_seq_hi_variant',
        'get_clock_seq_low', 'get_fields', 'get_hex', 'get_node', 'get_time',
        'get_time_hi_version', 'get_time_low', 'get_time_mid', 'get_urn',
        'get_variant', 'get_version']
    def _check_method(func_name, method):
        u = getattr(libuuid, func_name)()
        c = uuid.UUID(bytes=u.bytes)
        assert getattr(u, method)() == getattr(c, method)()
    for method in _METHODS:
        yield _check_method, 'uuid1', method
        yield _check_method, 'uuid4', method


def test_constants():
    _CONSTANTS = ['NAMESPACE_DNS', 'NAMESPACE_OID', 'NAMESPACE_URL',
                  'NAMESPACE_X500', 'RESERVED_FUTURE', 'RESERVED_MICROSOFT',
                  'RESERVED_NCS', 'RFC_4122']
    def _check_constant(const):
        assert getattr(libuuid, const) == getattr(uuid, const)
    for constant in _CONSTANTS:
        yield _check_constant, constant


class TestUUID(unittest.TestCase):

    def test_uuid1(self):
        u = libuuid.uuid1()
        u2 = uuid.UUID(bytes=u.bytes)
        self.assertEqual(u.bytes, u2.bytes)

    def test_uuid4(self):
        u = libuuid.uuid4()
        u2 = uuid.UUID(bytes=u.bytes)
        self.assertEqual(u.bytes, u2.bytes)

    def test_is_UUID_instance(self):
        u = libuuid.uuid4()
        self.assert_(isinstance(u, uuid.UUID))

    def test_uuid4_args_unsupported(self):
        self.assertRaises(NotImplementedError, lambda: libuuid.uuid1(42))
        self.assertRaises(NotImplementedError, lambda: libuuid.uuid1(42, 42))
        self.assertRaises(NotImplementedError, lambda: libuuid.uuid1(node=42))
        self.assertRaises(NotImplementedError, lambda: libuuid.uuid1(clock_seq=42))
        self.assertRaises(NotImplementedError, lambda: libuuid.uuid1(node=42, clock_seq=42))

    def test_uuid1_bytes(self):
        b = libuuid.uuid1_bytes()
        self.assertEquals(type(b), str)
        self.assertEquals(uuid.UUID(bytes=b).version, 1)

    def test_uuid4_bytes(self):
        b = libuuid.uuid4_bytes()
        self.assertEquals(type(b), str)
        self.assertEquals(uuid.UUID(bytes=b).version, 4)

    def test_basic_sanity_uuid4(self):
        buf = set()
        for _ in xrange(10000):
            u = libuuid.uuid4_bytes()
            self.assert_(u not in buf)
            buf.add(u)

    def test_basic_sanity_uuid1(self):
        buf = set()
        clocks = []
        for _ in xrange(1000):
            u = libuuid.uuid1()
            clocks.append(u.time)
            self.assert_(u.bytes not in buf)
            buf.add(u.bytes)
        self.assertEquals(clocks, sorted(clocks), "Timestamps increment")
        t = (time.time() * 1e7) + 0x01b21dd213814000L  # RFC 4122 timestamp
        diff = abs(t - clocks[-1])
        self.assert_(diff < 10000, "Timestamp reasonable")

    def test_multiple_threads(self):
        q = Queue()
        def _runsome():
            for _ in xrange(200):
                q.put(libuuid.uuid4().hex)
                q.put(libuuid.uuid1().hex)
        threads = [Thread(target=_runsome) for _ in xrange(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        result = list(q.queue)
        self.assertEquals(len(result), len(set(result)))

