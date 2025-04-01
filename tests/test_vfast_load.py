from av.vfast import vfast_load, get_stats
import numpy as np
import time

def main(video_path):

    d = get_stats(video_path)

    indices = list(range(0,d["num_frames"], 25))

    s = time.time()
    # be careful about hitting swap memory
    data = vfast_load(video_path, indices=indices, height=360, width=360, num_threads=4)
    e = time.time()
    
    print(data.shape)
    print(f"Timing was: {e-s}")

if __name__ == "__main__":
    from pathlib import Path

    home_dir = Path.home()
    mp4_files = home_dir.rglob("*.mp4")  # Recursively search for .mp4 files
    file = next(mp4_files)
    
    print(f"Testing {file}")
    main(file)