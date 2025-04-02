import deepcodec
import deepcodec.datasets

content = deepcodec.datasets.curated("pexels/time-lapse-video-of-night-sky-857195.mp4")
with deepcodec.open(content) as container:
    # Signal that we only want to look at keyframes.
    stream = container.streams.video[0]
    stream.codec_context.skip_frame = "NONKEY"

    for i, frame in enumerate(container.decode(stream)):
        print(frame)
        frame.to_image().save(f"night-sky.{i:04d}.jpg", quality=80)
