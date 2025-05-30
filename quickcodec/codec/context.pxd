cimport libav as lib
from libc.stdint cimport int64_t

from quickcodec.bytesource cimport ByteSource
from quickcodec.codec.codec cimport Codec
from quickcodec.codec.hwaccel cimport HWAccel
from quickcodec.frame cimport Frame
from quickcodec.packet cimport Packet


cdef class CodecContext:
    cdef lib.AVCodecContext *ptr

    # Whether AVCodecContext.extradata should be de-allocated upon destruction.
    cdef bint extradata_set

    # Used as a signal that this is within a stream, and also for us to access that
    # stream. This is set "manually" by the stream after constructing this object.
    cdef int stream_index

    cdef lib.AVCodecParserContext *parser
    cdef _init(self, lib.AVCodecContext *ptr, const lib.AVCodec *codec, HWAccel hwaccel)

    # Public API.
    cdef readonly bint is_open
    cdef readonly Codec codec
    cdef readonly HWAccel hwaccel
    cdef public dict options
    cpdef open(self, bint strict=?)

    # Wraps both versions of the transcode API, returning lists.
    cpdef encode(self, Frame frame=?)
    cpdef decode(self, Packet packet=?)
    cpdef flush_buffers(self)

    # Used by hardware-accelerated decode.
    cdef HWAccel hwaccel_ctx

    # Used by both transcode APIs to setup user-land objects.
    # TODO: Remove the `Packet` from `_setup_decoded_frame` (because flushing packets
    # are bogus). It should take all info it needs from the context and/or stream.
    cdef _prepare_and_time_rebase_frames_for_encode(self, Frame frame)
    cdef _prepare_frames_for_encode(self, Frame frame)
    cdef _setup_encoded_packet(self, Packet)
    cdef _setup_decoded_frame(self, Frame, Packet)

    # Implemented by base for the generic send/recv API.
    # Note that the user cannot send without receiving. This is because
    # `_prepare_frames_for_encode` may expand a frame into multiple (e.g. when
    # resampling audio to a higher rate but with fixed size frames), and the
    # send/recv buffer may be limited to a single frame. Ergo, we need to flush
    # the buffer as often as possible.
    cdef _recv_packet(self)
    cdef _send_packet_and_recv(self, Packet packet)
    cdef _recv_frame(self)

    cdef _transfer_hwframe(self, Frame frame)

    # Implemented by children for the generic send/recv API, so we have the
    # correct subclass of Frame.
    cdef Frame _next_frame
    cdef Frame _alloc_next_frame(self)

cdef CodecContext wrap_codec_context(lib.AVCodecContext*, const lib.AVCodec*, HWAccel hwaccel)
