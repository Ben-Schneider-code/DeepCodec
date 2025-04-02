cimport libav as lib

from deepcodec.descriptor cimport Descriptor


cdef class Filter:

    cdef const lib.AVFilter *ptr

    cdef object _inputs
    cdef object _outputs
    cdef Descriptor _descriptor


cdef Filter wrap_filter(const lib.AVFilter *ptr)
