cimport libav as lib

from deepcodec.container.core cimport Container
from deepcodec.stream cimport Stream


cdef class InputContainer(Container):

    cdef flush_buffers(self)
