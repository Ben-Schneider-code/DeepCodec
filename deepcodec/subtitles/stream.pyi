from deepcodec.packet import Packet
from deepcodec.stream import Stream
from deepcodec.subtitles.subtitle import SubtitleSet

class SubtitleStream(Stream):
    def decode(self, packet: Packet | None = None) -> list[SubtitleSet]: ...
