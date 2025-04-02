from deepcodec.packet cimport Packet
from deepcodec.stream cimport Stream


cdef class SubtitleStream(Stream):
    cpdef decode(self, Packet packet=?)
