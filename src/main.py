# src/main.py

import cv2
import threading
import time
import keyboard
from switcher.switcher import switch_module, switch_sub_mode, audio_handler
from speaker.tts import start_audio_thread

current_mode = 0
modes = [1, 2, 3, 4, 5]  # Corresponds to the modes: Face Recognition, Object Detection, Depth Sense, OCR, Sleep Mode

def main():
    global cap, lock, stop_event, current_mode, modes

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

    try:
        while True:
            if keyboard.is_pressed('enter'):
                current_mode = (current_mode + 1) % len(modes)
                print(f'Switching to mode {modes[current_mode]}')
                switch_module(modes[current_mode], cap, lock, stop_event)
                time.sleep(0.1)  # Add a short delay
            elif keyboard.is_pressed('tab'):
                current_mode = (current_mode - 1 + len(modes)) % len(modes)
                print(f'Switching to mode {modes[current_mode]}')
                switch_module(modes[current_mode], cap, lock, stop_event)
                time.sleep(0.1)  # Add a short delay
            elif keyboard.is_pressed('page up'):
                print("Submode + ")
                if modes[current_mode] in [1, 2]:  # Face Recognition and Object Detection modes have sub-modes
                    switch_sub_mode(1, modes[current_mode], cap, lock, stop_event)
                    time.sleep(0.1)  # Add a short delay
            elif keyboard.is_pressed('page down'):
                print("Submode - ")
                if modes[current_mode] in [1, 2]:  # Face Recognition and Object Detection modes have sub-modes
                    switch_sub_mode(-1, modes[current_mode], cap, lock, stop_event)
                    time.sleep(0.1)  # Add a short delay
            time.sleep(0.01)  # Short delay to reduce CPU usage
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        stop_event.set()
        cap.release()
        cv2.destroyAllWindows()
        audio_handler.stop()
        audio_thread.join()

if __name__ == "__main__":
    main()
