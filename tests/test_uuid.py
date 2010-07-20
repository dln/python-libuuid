# -*- coding: utf-8 -*-
from random import choice, randrange
import os
import shutil
import string
import sys
import tempfile
import time
import unittest
import uuid

import libuuid


def test_properties():
    _PROPERTIES = [
        'bytes', 'bytes_le', 'clock_seq', 'clock_seq_hi_variant',
        'clock_seq_low', 'fields', 'hex', 'node', 'time', 'time_hi_version',
        'time_low', 'time_mid', 'urn', 'variant', 'version'
    ]

    def _check_property(factory_func, prop):
        u = factory_func()
        u2 = uuid.UUID(bytes=u.bytes)
        a1 = getattr(u, prop)
        a2 = getattr(u2, prop)
        assert a1 == a2

    for prop in _PROPERTIES:
        test_properties.__doc__ = "Property: " + prop
        yield _check_property, libuuid.uuid1, prop
        yield _check_property, libuuid.uuid4, prop

def test_methods():
    _METHODS = [
        '__hash__', '__int__', '__repr__', '__str__', 'get_bytes',
        'get_bytes_le', 'get_clock_seq', 'get_clock_seq_hi_variant',
        'get_clock_seq_low', 'get_fields', 'get_hex', 'get_node', 'get_time',
        'get_time_hi_version', 'get_time_low', 'get_time_mid', 'get_urn',
        'get_variant', 'get_version'
    ]

    def _check_method(factory_func, method, *args, **kwargs):
        u = factory_func()
        u2 = uuid.UUID(bytes=u.bytes)
        m1 = getattr(u, method)(*args, **kwargs)
        m2 = getattr(u2, method)(*args, **kwargs)
        assert m1 == m2

    for method in _METHODS:
        test_methods.__doc__ = "Method: " + method
        yield _check_method, libuuid.uuid1, method
        yield _check_method, libuuid.uuid4, method


def test_constants():

    _CONSTANTS = ['NAMESPACE_DNS', 'NAMESPACE_OID', 'NAMESPACE_URL',
                  'NAMESPACE_X500', 'RESERVED_FUTURE', 'RESERVED_MICROSOFT',
                  'RESERVED_NCS', 'RFC_4122']

    def _check_constant(const):
        m1 = getattr(libuuid, const)
        m2 = getattr(uuid, const)
        assert m1 == m2

    for constant in _CONSTANTS:
        test_methods.__doc__ = "Constant: " + constant
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





