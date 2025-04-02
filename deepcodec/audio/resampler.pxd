from deepcodec.audio.format cimport AudioFormat
from deepcodec.audio.frame cimport AudioFrame
from deepcodec.audio.layout cimport AudioLayout
from deepcodec.filter.graph cimport Graph


cdef class AudioResampler:

    cdef readonly bint is_passthrough

    cdef AudioFrame template

    # Destination descriptors
    cdef readonly AudioFormat format
    cdef readonly AudioLayout layout
    cdef readonly int rate
    cdef readonly unsigned int frame_size

    cdef Graph graph

    cpdef resample(self, AudioFrame)
