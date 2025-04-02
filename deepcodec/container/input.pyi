from typing import Any, Iterator, overload

from deepcodec.audio.frame import AudioFrame
from deepcodec.audio.stream import AudioStream
from deepcodec.packet import Packet
from deepcodec.stream import Stream
from deepcodec.subtitles.stream import SubtitleStream
from deepcodec.subtitles.subtitle import SubtitleSet
from deepcodec.video.frame import VideoFrame
from deepcodec.video.stream import VideoStream

from .core import Container

class InputContainer(Container):
    start_time: int
    duration: int | None
    bit_rate: int
    size: int

    def __enter__(self) -> InputContainer: ...
    def close(self) -> None: ...
    def demux(self, *args: Any, **kwargs: Any) -> Iterator[Packet]: ...
    @overload
    def decode(self, video: int) -> Iterator[VideoFrame]: ...
    @overload
    def decode(self, audio: int) -> Iterator[AudioFrame]: ...
    @overload
    def decode(self, subtitles: int) -> Iterator[SubtitleSet]: ...
    @overload
    def decode(self, *args: VideoStream) -> Iterator[VideoFrame]: ...
    @overload
    def decode(self, *args: AudioStream) -> Iterator[AudioFrame]: ...
    @overload
    def decode(self, *args: SubtitleStream) -> Iterator[SubtitleSet]: ...
    @overload
    def decode(
        self, *args: Any, **kwargs: Any
    ) -> Iterator[VideoFrame | AudioFrame | SubtitleSet]: ...
    def seek(
        self,
        offset: int,
        *,
        backward: bool = True,
        any_frame: bool = False,
        stream: Stream | VideoStream | AudioStream | None = None,
        unsupported_frame_offset: bool = False,
        unsupported_byte_offset: bool = False,
    ) -> None: ...
    def flush_buffers(self) -> None: ...
