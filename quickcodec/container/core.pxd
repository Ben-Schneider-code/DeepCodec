cimport libav as lib

from quickcodec.codec.hwaccel cimport HWAccel
from quickcodec.container.pyio cimport PyIOFile
from quickcodec.container.streams cimport StreamContainer
from quickcodec.dictionary cimport _Dictionary
from quickcodec.format cimport ContainerFormat
from quickcodec.stream cimport Stream

# Interrupt callback information, times are in seconds.
ctypedef struct timeout_info:
    double start_time
    double timeout


cdef class Container:

    cdef readonly bint writeable
    cdef lib.AVFormatContext *ptr

    cdef readonly object name
    cdef readonly str metadata_encoding
    cdef readonly str metadata_errors

    cdef readonly PyIOFile file
    cdef int buffer_size
    cdef bint input_was_opened
    cdef readonly object io_open
    cdef readonly object open_files

    cdef readonly ContainerFormat format

    cdef readonly dict options
    cdef readonly dict container_options
    cdef readonly list stream_options

    cdef HWAccel hwaccel

    cdef readonly StreamContainer streams
    cdef readonly dict metadata

    # Private API.
    cdef _assert_open(self)
    cdef int err_check(self, int value) except -1

    # Timeouts
    cdef readonly object open_timeout
    cdef readonly object read_timeout
    cdef timeout_info interrupt_callback_info
    cdef set_timeout(self, object)
    cdef start_timeout(self)
