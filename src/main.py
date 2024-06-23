# src/main.py

import cv2
import threading
import time
from pynput import keyboard
from switcher.switcher import switch_module, switch_sub_mode, audio_handler
from speaker.tts import start_audio_thread

current_mode = 0
modes = [1, 2, 3, 4, 5]  # Corresponds to the modes: Face Recognition, Object Detection, Depth Sense, OCR, Sleep Mode

def on_press(key):
    global current_mode
    try:
        if key == keyboard.Key.enter:
            current_mode = (current_mode + 1) % len(modes)
            print(f'Switching to mode {current_mode + 1}')
            switch_module(modes[current_mode], cap, lock, stop_event)
            time.sleep(0.1)  # Add a short delay
        elif key == keyboard.Key.tab:
            current_mode = (current_mode - 1) % len(modes)
            print(f'Switching to mode {current_mode + 1}')
            switch_module(modes[current_mode], cap, lock, stop_event)
            time.sleep(0.1)  # Add a short delay
        elif key == keyboard.Key.page_up:
            if current_mode in [1, 2]:  # Face Recognition and Object Detection modes have sub-modes
                switch_sub_mode(1, current_mode,cap, lock, stop_event)
                time.sleep(0.1)  # Add a short delay
        elif key == keyboard.Key.page_down:
            if current_mode in [1, 2]:  # Face Recognition and Object Detection modes have sub-modes
                switch_sub_mode(-1, cap, lock, stop_event)
                time.sleep(0.1)  # Add a short delay
    except AttributeError:
        pass

def main():
    global cap, lock, stop_event

    # Initialize the camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    lock = threading.Lock()
    stop_event = threading.Event()
    audio_handler.add_audio_task("Starting-Aurasense")
    # Start the audio thread
    audio_thread = start_audio_thread(audio_handler)

    # Start the keyboard listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    try:
        while True:
            # This loop runs continuously, the keyboard listener handles mode switching
            pass
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        stop_event.set()
        cap.release()
        cv2.destroyAllWindows()
        audio_handler.stop()
        audio_thread.join()
        listener.stop()

if __name__ == "__main__":
    main()
