cimport libav as lib

from deepcodec.codec.context cimport CodecContext
from deepcodec.container.core cimport Container
from deepcodec.frame cimport Frame
from deepcodec.packet cimport Packet


cdef class Stream:
    cdef lib.AVStream *ptr

    # Stream attributes.
    cdef readonly Container container
    cdef readonly dict metadata

    # CodecContext attributes.
    cdef readonly CodecContext codec_context

    # Private API.
    cdef _init(self, Container, lib.AVStream*, CodecContext)
    cdef _finalize_for_output(self)
    cdef _set_time_base(self, value)
    cdef _set_id(self, value)


cdef Stream wrap_stream(Container, lib.AVStream*, CodecContext)
