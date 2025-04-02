from typing import Literal

from deepcodec.codec.context import CodecContext

class SubtitleCodecContext(CodecContext):
    type: Literal["subtitle"]
