# src/main.py

import cv2
import threading
from switcher.switcher import switch_module, audio_handler
from speaker.tts import start_audio_thread

def main():
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
            print("Enter the module number to run (1: Face Recognition, 2: Object Detection, 3: Depth Sense, 4: OCR, 0: Exit):")
            try:
                module_number = int(input())
                if module_number == 0:
                    print("Exiting...")
                    stop_event.set()
                    audio_handler.stop()
                    break

                switch_module(module_number, cap, lock, stop_event)

            except ValueError:
                print("Please enter a valid number.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        audio_thread.join()

if __name__ == "__main__":
    main()
