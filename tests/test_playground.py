import time
import traceback
import multiprocessing.shared_memory
from multiprocessing.resource_tracker import _resource_tracker




video_path = "/home/bsch/20min.mp4"
height = 360
width = 224
max_num_threads = [1]


for thread in max_num_threads:
        from deepcodec import VideoReader
        vr = VideoReader(video_path, num_threads=thread)
        indices = list(range(0,len(vr), 25))
        s = time.time()
        b = vr.get_batch(indices)
        e = time.time()
        print(b)
        print(f"DeepCodec [spawn] took {e-s} with {thread} threads")
        print(b.shape)
            