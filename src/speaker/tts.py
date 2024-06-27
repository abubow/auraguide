# src/speaker/tts.py

import threading
import queue
import time
import os
from pydub import AudioSegment
import simpleaudio as sa
from pydub import AudioSegment
from pydub import playback as sa

class AudioHandler:
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.stop_event = threading.Event()

    def add_audio_task(self, audio_file):
        self.audio_queue.put(audio_file)

    def run(self):
        while not self.stop_event.is_set():
            try:
                audio_file = self.audio_queue.get(timeout=1)  # wait for 1 second
                # check if file exists
                path = "src/data/audios/" + audio_file + ".wav"
                path = "src/data/audios/" + audio_file + ".wav"
                if os.path.exists(path):
                    audio_segment = AudioSegment.from_wav(path)
                    play_obj = sa.play_buffer(
                        audio_segment.raw_data,
                        num_channels=audio_segment.channels,
                        bytes_per_sample=audio_segment.sample_width,
                        sample_rate=audio_segment.frame_rate
                    )
                    play_obj.wait_done()  # Wait until playback is finished
                    audio_segment = AudioSegment.from_wav(path)
                    sa.play(audio_segment)
                else:
                    print(os.listdir("../"))
                    print(path, " not found.")
            except queue.Empty:
                continue

    def stop(self):
        self.stop_event.set()

def start_audio_thread(audio_handler):
    audio_thread = threading.Thread(target=audio_handler.run)
    audio_thread.start()
    return audio_thread