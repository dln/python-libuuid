# Python bindings for libavro

cdef extern from *:
    ctypedef char* const_char_ptr "const char*"

cdef extern from "stdint.h" nogil:
    ctypedef int int32_t
    ctypedef int uint32_t

cdef extern from 'stdio.h' nogil:
    int snprintf(char *str, size_t size, char *format, ...)

cdef extern from "stdlib.h" nogil:
    void free(void * ptr)
    void * malloc(int size)

cdef extern from "string.h" nogil:
    void *memset(void *, int, size_t)

cdef extern from 'sys/time.h' nogil:
    ctypedef struct timeval:
        unsigned int tv_sec
        unsigned int tv_usec
    ctypedef int32_t time_t

# UUID Variant definitions 
UUID_VARIANT_NCS = 0
UUID_VARIANT_DCE = 1
UUID_VARIANT_MICROSOFT = 2
UUID_VARIANT_OTHER = 3

# UUID Type definitions
UUID_TYPE_DCE_TIME = 1
UUID_TYPE_DCE_RANDOM = 4

cdef extern from 'uuid/uuid.h' nogil:
    ctypedef unsigned char uuid_t[16]

    void uuid_clear(uuid_t uu)

    int uuid_compare(uuid_t uu1, uuid_t uu2)

    void uuid_copy(uuid_t dst, uuid_t src)

    void uuid_generate(uuid_t out)
    void uuid_generate_random(uuid_t out)
    void uuid_generate_time(uuid_t out)

    int uuid_is_null(uuid_t uu)

    int uuid_parse(const_char_ptr indata, uuid_t uu)

    void uuid_unparse(uuid_t uu, char *out)
    void uuid_unparse_lower(uuid_t uu, char *out)
    void uuid_unparse_upper(uuid_t uu, char *out)

    time_t uuid_time(uuid_t uu, timeval *ret_tv)
    int uuid_type(uuid_t uu)
    int uuid_variant(uuid_t uu)

