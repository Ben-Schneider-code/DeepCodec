from deepcodec.plane cimport Plane
from deepcodec.video.format cimport VideoFormatComponent


cdef class VideoPlane(Plane):

    cdef readonly size_t buffer_size
    cdef readonly unsigned int width, height
