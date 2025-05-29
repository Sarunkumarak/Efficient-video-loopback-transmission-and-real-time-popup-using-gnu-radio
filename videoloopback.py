import subprocess
import threading
import time
import os
from gnuradio import gr
import numpy as np

class blk(gr.sync_block):  # You can also use basic_block
    def __init__(self):
        gr.sync_block.__init__(self,
            name="Play Video",
            in_sig=[np.float32],   # Match float input
            out_sig=[np.float32])  # Dummy output
        self.video_played = False

    def start(self):
        if not self.video_played:
            self.video_played = True
            threading.Thread(target=self.play_video, daemon=True).start()
        return super().start()

    def play_video(self):
        try:
            video_path = "/home/arunkumar-ak/Videos/ajith.mp4"
            output_path = "/home/arunkumar-ak/Videos/ajith1.mp4"

            if os.path.exists(video_path):
                subprocess.run(["chmod", "+r", video_path], check=True)
                subprocess.run(["chmod", "+w", "/home/arunkumar-ak/Videos/"], check=True)

                subprocess.run([
                    "ffmpeg", "-y", "-loglevel", "error",
                    "-i", video_path,
                    "-c:v", "libx264", "-preset", "slow",
                    "-c:a", "aac", "-strict", "-2",
                    output_path
                ], check=True)

                time.sleep(1)

                subprocess.run([
                    "ffplay", "-autoexit", output_path
                ], check=True)
            else:
                print("Video file not found!")
        except subprocess.CalledProcessError as e:
            print("Error during video play:", e)

    def work(self, input_items, output_items):
        # Just forward the input to output
        output_items[0][:] = input_items[0]
        return len(output_items[0])









