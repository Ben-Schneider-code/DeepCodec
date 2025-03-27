from .container import open
import bisect
from typing import Set, Dict

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
        'duration': round(total_duration/num_packet),
    }

def compute_parellelized_intervals(video_path: str, width: int = -1, height: int = 1, num_threads: int = 1):

    d: Dict = get_stats(video_path)
    assert type(num_threads) is int and num_threads > 0

    interval: float = (d["end"] - d["start"]) / num_threads
    kf: list = d["kf"]
    s: Set = set()

    for i in range(1, num_threads):
        apx_pts: float = interval * i
        idx: int = bisect.bisect_right(kf, apx_pts)
        print(apx_pts)
        # Null guard
        if not (idx == 0 or idx == len(kf)):

            # add closest approximation
            if abs(kf[idx-1]-apx_pts) < abs(kf[idx]-apx_pts):
                s.add(kf[idx-1])
            else: 
                s.add(kf[idx])
    
    print("fin")

    s.add(d["start"])
    s.add(d['end'])
    s = sorted(list(s))
    s = [(s[i], s[i+1]) for i in range(len(s)-1)]

    return s

def estimate_frame_location(pts: int, pts_start: int, pts_end: int, num_frames: int)-> int:
    """
    Convert the pts of a frame to its index location.
    """
    return round((num_frames-1)* pts / (pts_end-pts_start))
    #return ((num_frames-1)*(pts) //  (pts_end-pts_start))