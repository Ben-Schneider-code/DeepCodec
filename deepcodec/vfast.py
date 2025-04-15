from .container import open, parallel_open
import bisect
from typing import Set, Dict
from multiprocessing import shared_memory
import numpy as np
import subprocess
import os
import base64
import pickle

def vfast_load(video_path, indices: list | None = None, height=0, width=0, num_threads=1, d=None, spawn_method: str = "fork"):
    assert height > 0, "currently we need these set up front to allocate the buffer"
    assert width > 0, "currently we need these set up front to allocate the buffer"
    
    intervals, metadata, indices = compute_parellelized_intervals(video_path, indices, num_threads, d=d)
    batch_map = {y: x for (x, y) in enumerate(indices)}
    processes = []
    pickled = pickle.dumps(batch_map, protocol=5)
    pickled = base64.b64encode(pickled).decode('utf-8')
    shape = (len(batch_map), 3, height, width)
    my_dtype = np.uint8
    arr = np.zeros(shape, dtype=my_dtype)
    shm = None
    
    try:
        shm = shared_memory.SharedMemory(create=True, size=arr.size)
        shared_array = np.ndarray(shape, dtype=my_dtype, buffer=shm.buf)

        for rank, (x, y, buffer_size) in enumerate(intervals):
            process = subprocess.Popen(["deepcodec",
                                        video_path,
                                        shm.name,
                                        pickled,
                                        str(x),
                                        str(y),
                                        str(buffer_size),
                                        str(height),
                                        str(width),
                                        str(metadata["num_frames"]),
                                        str(rank),
                                        str(len(intervals)),
                                        str(metadata["start"]),
                                        str(metadata["end"])])
            processes.append(process)
        for wait_process in processes:
            wait_process.wait()
        
        np.copyto(arr, shared_array)
    finally:
        if shm is not None:
            shm.close()
            shm.unlink()
    return arr

def get_stats(video_path):
    container = open(video_path)
    video_stream = container.streams.video[0]
    num_frames = video_stream.frames
    
    assert num_frames > 0, "The metadata reported that the video stream has 0 frames"

    keyframes = []
    end_pts = -1
    start_pts = float('inf')

    for packet in container.demux():
        if packet.stream.type == 'video':
            if packet.pts is None:
                continue


            if packet.pts > end_pts:
                end_pts = packet.pts

            if packet.pts < start_pts:
                start_pts = packet.pts

            if packet.is_keyframe:
                keyframes.append(packet.pts)


    return {
        'kf': keyframes,
        'start': start_pts,
        'end': end_pts,
        'num_frames': num_frames,
        'height': video_stream.height,
        'width': video_stream.width,
        'fps': video_stream.average_rate
    }

def compute_parellelized_intervals(video_path: str, indicies: list | None, num_threads: int = 1, d : dict | None = None):

    if d is None:
        d = get_stats(video_path)

    assert type(num_threads) is int and num_threads > 0

    if indicies is None:
        indicies = list(range(d["num_frames"]))

    interval: float = (d["end"] - d["start"]) / num_threads
    kf: list = d["kf"]
    s = set()

    for i in range(1, num_threads):
        apx_pts: float = interval * i
        idx: int = bisect.bisect_right(kf, apx_pts)
        # Null guard
        if not (idx == 0 or idx == len(kf)):

            # add closest approximation
            if abs(kf[idx-1]-apx_pts) < abs(kf[idx]-apx_pts):
                s.add(kf[idx-1])
            else: 
                s.add(kf[idx])

    s.add(d["start"])
    s.add(d['end'])
    s = sorted(list(s))

    ret = []
    for i in range(len(s)-1):

        start_frame = estimate_frame_location(s[i], d["start"], d["end"], d["num_frames"])
        end_frame = estimate_frame_location(s[i+1], d["start"], d["end"], d["num_frames"])

        idx_start = bisect.bisect_left(indicies, start_frame)
        idx_end = bisect.bisect_left(indicies,end_frame)

        buffer_size = idx_end-idx_start
        
        # adjust buffer size for when the last interval will load the very last frame
        if i == len(s)-2 and indicies[-1] == d["num_frames"]-1:
            buffer_size += 1
        
        ret.append((s[i], s[i+1], buffer_size))


    return ret, d, indicies

def estimate_frame_location(pts: int, pts_start: int, pts_end: int, num_frames: int)-> int:
    """
    Convert the pts of a frame to its index location.
    """
    return round((num_frames-1)* pts / (pts_end-pts_start))

class VideoReader:

    def __init__(self,
                video_path: str,
                height: int = 0,
                width: int = 0,
                num_threads=4):
        
        self.video_path = video_path
        self.num_threads = num_threads
        self.video_metadata = get_stats(video_path)
        self.height = height if height > 0 else self.video_metadata["height"]
        self.width = width if width > 0 else self.video_metadata["width"]
        self.spawn_method = "fork"

    def framecount(self) -> int:
        return self.video_metadata["num_frames"]

    def __len__(self) -> int:
        return self.video_metadata["num_frames"]

    def get_fps(self):
        return self.video_metadata["fps"]

    def get_batch(self, indices: list[int]) -> np.Array:
        return vfast_load(self.video_path, indices, self.height, self.width, self.num_threads, self.video_metadata, self.spawn_method)