cimport libav as lib

from deepcodec.buffer cimport Buffer
from deepcodec.bytesource cimport ByteSource
from deepcodec.stream cimport Stream


cdef class Packet(Buffer):

    cdef lib.AVPacket* ptr

    cdef Stream _stream

    # We track our own time.
    cdef lib.AVRational _time_base
    cdef _rebase_time(self, lib.AVRational)

    # Hold onto the original reference.
    cdef ByteSource source
    cdef size_t _buffer_size(self)
    cdef void* _buffer_ptr(self)
