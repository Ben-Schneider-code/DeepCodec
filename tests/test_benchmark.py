import time
import traceback

def main():
    video_path = "/home/bsch/20min.mp4"
    height = 360
    width = 224
    max_num_threads = [8,4,2]
    indices = list(range(0,91500, 25))

    for thread in max_num_threads:

        print(f"\n===== Testing with {thread} threads =====")


        # TorchCodec
        try:
            import torch
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
    
            vr = VideoReader(video_path, num_threads=thread)
            s = time.time()
            b = vr.get_batch(indices)
            e = time.time()
            print(f"DeepCodec [spawn] took {e-s} with {thread} threads")
            print(b.shape)

        except Exception as e:
            print(traceback.format_exc())
            print(e)
            print("DeepCodec error")        

        # Decord
        try:
            import decord
            from decord import VideoReader as DecordVideoReader
            from decord import cpu

            s = time.time()
            vr = DecordVideoReader(video_path, ctx=cpu(0), height=height, width=width, num_threads=thread)
            frames = vr.get_batch(indices)
            e = time.time()

            print(f"Decord took {e - s:.2f} seconds with {thread} threads")

        except Exception as e:
            print(e)
            print("Decord error")


if __name__ == "__main__":
    #freeze_support()
    main()