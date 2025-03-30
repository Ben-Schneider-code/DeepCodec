from av.vfast import vfast_load
import numpy as np
import time

def main(video_path):
    s = time.time()
    vfast_load(video_path, num_threads=8)
    e = time.time()
    
    print(f"Timing was: {e-s}")

if __name__ == "__main__":
    from pathlib import Path

    home_dir = Path.home()
    mp4_files = home_dir.rglob("*.mp4")  # Recursively search for .mp4 files
    file = next(mp4_files)
    
    print(f"Testing {file}")
    main(file)