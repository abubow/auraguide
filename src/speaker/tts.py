# src/speaker/tts.py

import threading
import queue
import time
import pygame
import os

class AudioHandler:
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.stop_event = threading.Event()
        pygame.mixer.init()

    def add_audio_task(self, audio_file):
        self.audio_queue.put(audio_file)

    def run(self):
        while not self.stop_event.is_set():
            try:
                audio_file = self.audio_queue.get(timeout=1)  # wait for 1 second
                # check if file exists
                path = "src/data/audios/"+audio_file+".wav"
                if os.path.exists(path):
                    pygame.mixer.music.load(path)
                    pygame.mixer.music.play()
                else:
                    print(os.listdir("../"))
                    print(path, " not found.")
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
            except queue.Empty:
                continue

    def stop(self):
        self.stop_event.set()

def start_audio_thread(audio_handler):
    audio_thread = threading.Thread(target=audio_handler.run)
    audio_thread.start()
    return audio_thread