from .container import open, parallel_open
import bisect
from typing import Set, Dict
import numpy as np
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

def wrap(inputs):
    return parallel_open(*inputs)

def vfast_load(video_path, indices: list | None = None, height=0,  width=0,  num_threads=1):

    assert height > 0, "currently we need these set up front to allocate the buffer"
    assert width > 0, "currently we need these set up front to allocate the buffer"

    if indices is None:
        indices = list(range(metadata["num_frames"]))
    

    batch_map = {y:x for (x,y) in enumerate(indices)}

    intervals, metadata = compute_parellelized_intervals(video_path, indices, num_threads)

    # make this a fork
    ctx = mp.get_context("spawn")

    inputs, data = [],[]

    for rank, (x,y, buffer_size) in enumerate(intervals):
        inputs.append((video_path, batch_map,x,y,buffer_size, height, width, metadata["num_frames"],rank, len(intervals), metadata["start"], metadata["end"]))

    with ProcessPoolExecutor(max_workers=len(intervals), mp_context=ctx) as executor:
        data = [item for item in list(executor.map(wrap, inputs))]

    exit()
    return np.concatenate(data, axis=0)

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
    }

def compute_parellelized_intervals(video_path: str, indicies: list, num_threads: int = 1):

    d: Dict = get_stats(video_path)
    assert type(num_threads) is int and num_threads > 0

    interval: float = (d["end"] - d["start"]) / num_threads
    kf: list = d["kf"]
    s: Set = set()

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

        start_frame = estimate_frame_location(s[i])
        end_frame = estimate_frame_location(s[i+1])

        idx_start = bisect.bisect_left(indicies, start_frame)
        idx_end = bisect.bisect_left(indicies,end_frame)

        buffer_size = idx_end-idx_start
        
        # adjust buffer size for when the last interval will load the very last frame
        if i == len(s)-2 and indicies[-1] == d["num_frames"]-1:
            buffer_size += 1
        
        ret.append(s[i], s[i+1], buffer_size)


    return ret, d

def estimate_frame_location(pts: int, pts_start: int, pts_end: int, num_frames: int)-> int:
    """
    Convert the pts of a frame to its index location.
    """
    return round((num_frames-1)* pts / (pts_end-pts_start))