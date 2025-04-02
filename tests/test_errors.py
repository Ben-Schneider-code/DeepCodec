import errno
from traceback import format_exception_only

import deepcodec

from .common import is_windows


def test_stringify() -> None:
    for cls in (deepcodec.ValueError, deepcodec.FileNotFoundError, deepcodec.DecoderNotFoundError):
        e = cls(1, "foo")
        assert f"{e}" == "[Errno 1] foo"
        assert f"{e!r}" == f"{cls.__name__}(1, 'foo')"
        assert (
            format_exception_only(cls, e)[-1]
            == f"av.error.{cls.__name__}: [Errno 1] foo\n"
        )

    for cls in (deepcodec.ValueError, deepcodec.FileNotFoundError, deepcodec.DecoderNotFoundError):
        e = cls(1, "foo", "bar.txt")
        assert f"{e}" == "[Errno 1] foo: 'bar.txt'"
        assert f"{e!r}" == f"{cls.__name__}(1, 'foo', 'bar.txt')"
        assert (
            format_exception_only(cls, e)[-1]
            == f"av.error.{cls.__name__}: [Errno 1] foo: 'bar.txt'\n"
        )


def test_bases() -> None:
    assert issubclass(deepcodec.ValueError, ValueError)
    assert issubclass(deepcodec.ValueError, deepcodec.FFmpegError)

    assert issubclass(deepcodec.FileNotFoundError, FileNotFoundError)
    assert issubclass(deepcodec.FileNotFoundError, OSError)
    assert issubclass(deepcodec.FileNotFoundError, deepcodec.FFmpegError)


def test_filenotfound():
    """Catch using builtin class on Python 3.3"""
    try:
        deepcodec.open("does not exist")
    except FileNotFoundError as e:
        assert e.errno == errno.ENOENT
        if is_windows:
            assert e.strerror in (
                "Error number -2 occurred",
                "No such file or directory",
            )
        else:
            assert e.strerror == "No such file or directory"
        assert e.filename == "does not exist"
    else:
        assert False, "No exception raised!"


def test_buffertoosmall() -> None:
    """Throw an exception from an enum."""

    BUFFER_TOO_SMALL = 1397118274
    try:
        deepcodec.error.err_check(-BUFFER_TOO_SMALL)
    except deepcodec.error.BufferTooSmallError as e:
        assert e.errno == BUFFER_TOO_SMALL
    else:
        assert False, "No exception raised!"
