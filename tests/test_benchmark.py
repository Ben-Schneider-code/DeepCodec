import time

video_path = "/home/bsch/60min.mp4"
hieght = 360
width = 360
max_num_threads = [8,4,2]
indices = list(range(0,91500, 25))

for thread in max_num_threads:

    # TorchCodec

    try:

        from torchcodec.decoders import VideoDecoder

        s = time.time()
        device = "cpu"
        decoder = VideoDecoder(video_path, device=device, num_ffmpeg_threads = thread)
        decoder.get_frames_at(indices=indices)
        e = time.time()

        print(f"TorchCodec took {e-s} with {thread} threads")

    except Exception as e:
        print(e)
        print("TorchCodec error")

    try:
        from deepcodec import VideoReader
        
        s = time.time()
        vr = VideoReader(video_path, 360, 360, num_threads=thread)
        vr.get_batch(indices)
        e = time.time()
        print(f"DeepCodec took {e-s} with {thread} threads")

    except Exception as e:
        print(e)
        print("DeepCodec error")
