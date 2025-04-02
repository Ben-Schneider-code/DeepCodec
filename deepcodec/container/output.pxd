cimport libav as lib

from deepcodec.container.core cimport Container
from deepcodec.stream cimport Stream


cdef class OutputContainer(Container):

    cdef bint _started
    cdef bint _done
    cdef lib.AVPacket *packet_ptr

    cpdef start_encoding(self)
