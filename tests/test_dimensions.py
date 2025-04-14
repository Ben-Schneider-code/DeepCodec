import time

video_path = "/home/bsch/60min.mp4"
height = 224
width = 224
max_num_threads = [16,8,4,2]
indices = list(range(0,91500, 25))


thread = 4

from deepcodec import VideoReader

s = time.time()
vr = VideoReader(video_path, height, width, num_threads=thread)
vr.get_batch(indices)
e = time.time()
print(f"DeepCodec took {e-s} with {thread} threads")
