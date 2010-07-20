# cython: embedsignature=True
import uuid as uuid_std

cimport uuid
from uuid cimport *

cdef extern from "Python.h":
    object PyString_FromFormat(char *format, ...)
    object PyString_FromStringAndSize(char *s, int len)
    object PyString_FromString(char *s)
    object PyLong_FromVoidPtr(void *p)
    object PyLong_FromString(char *, char**, int)
    object _PyLong_FromByteArray(unsigned char *bytes, unsigned int n,
                                 int little_endian, int is_signed)
    int _PyLong_AsByteArray(object v, unsigned char *bytes, unsigned int n,
                            int little_endian, int is_signed) except -1

    int PyString_Size(object s)
    object PyString_FromStringAndSize(char *, int)
    char *PyString_AS_STRING(object s)


class FastUUID(uuid_std.UUID):
    def __init__(self, version=4, *args, **kwargs):
        cdef object buf = PyString_FromStringAndSize(NULL, 16)
        cdef unsigned char *_bytes = <unsigned char*>PyString_AS_STRING(buf)
        if version == 1:
            uuid_generate_time(_bytes)
        elif version == 4:
            uuid_generate_random(_bytes)
        self.__dict__['bytes'] = buf
        self.__dict__['int'] = _PyLong_FromByteArray(_bytes, 16, 0, 0)

    def get_bytes(self):
        return self.bytes


def uuid1(node=None, clock_seq=None):
    if node or clock_seq:
        raise NotImplementedError, "node and clock_seq are not supported in libuuid"
    return FastUUID(1)

uuid3 = uuid_std.uuid3

uuid4 = FastUUID

uuid5 = uuid_std.uuid5

def uuid1_bytes():
    cdef object bytes = PyString_FromStringAndSize(NULL, 16)
    uuid_generate_time(<unsigned char*>PyString_AS_STRING(bytes))
    return bytes

def uuid4_bytes():
    cdef object bytes = PyString_FromStringAndSize(NULL, 16)
    uuid_generate_random(<unsigned char*>PyString_AS_STRING(bytes))
    return bytes


