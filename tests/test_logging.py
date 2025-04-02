import errno
import logging
import threading

import deepcodec.error
import deepcodec.logging


def do_log(message: str) -> None:
    deepcodec.logging.log(deepcodec.logging.INFO, "test", message)


def test_adapt_level() -> None:
    assert deepcodec.logging.adapt_level(deepcodec.logging.ERROR) == logging.ERROR
    assert deepcodec.logging.adapt_level(deepcodec.logging.WARNING) == logging.WARNING
    assert (
        deepcodec.logging.adapt_level((deepcodec.logging.WARNING + deepcodec.logging.ERROR) // 2)
        == logging.WARNING
    )


def test_threaded_captures() -> None:
    deepcodec.logging.set_level(deepcodec.logging.VERBOSE)

    with deepcodec.logging.Capture(local=True) as logs:
        do_log("main")
        thread = threading.Thread(target=do_log, args=("thread",))
        thread.start()
        thread.join()

    assert (deepcodec.logging.INFO, "test", "main") in logs
    deepcodec.logging.set_level(None)


def test_global_captures() -> None:
    deepcodec.logging.set_level(deepcodec.logging.VERBOSE)

    with deepcodec.logging.Capture(local=False) as logs:
        do_log("main")
        thread = threading.Thread(target=do_log, args=("thread",))
        thread.start()
        thread.join()

    assert (deepcodec.logging.INFO, "test", "main") in logs
    assert (deepcodec.logging.INFO, "test", "thread") in logs
    deepcodec.logging.set_level(None)


def test_repeats() -> None:
    deepcodec.logging.set_level(deepcodec.logging.VERBOSE)

    with deepcodec.logging.Capture() as logs:
        do_log("foo")
        do_log("foo")
        do_log("bar")
        do_log("bar")
        do_log("bar")
        do_log("baz")

    logs = [log for log in logs if log[1] == "test"]

    assert logs == [
        (deepcodec.logging.INFO, "test", "foo"),
        (deepcodec.logging.INFO, "test", "foo"),
        (deepcodec.logging.INFO, "test", "bar"),
        (deepcodec.logging.INFO, "test", "bar (repeated 2 more times)"),
        (deepcodec.logging.INFO, "test", "baz"),
    ]

    deepcodec.logging.set_level(None)


def test_error() -> None:
    deepcodec.logging.set_level(deepcodec.logging.VERBOSE)

    log = (deepcodec.logging.ERROR, "test", "This is a test.")
    deepcodec.logging.log(*log)
    try:
        deepcodec.error.err_check(-errno.EPERM)
    except deepcodec.error.PermissionError as e:
        assert e.log == log
    else:
        assert False

    deepcodec.logging.set_level(None)
