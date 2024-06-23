# src/switcher/switcher.py

import threading
import gc
import time
from face_recognition.face_recognition import recognize_faces, store_unknown_faces
from object_detection.object_detection import detect_objects, image_captioning
from depth_sense.depth_sense import sense_depth
from ocr.ocr import perform_ocr
from speaker.tts import AudioHandler

active_threads = []
audio_handler = AudioHandler()
current_sub_mode = 0  # Initialize current_sub_mode

# Define sub-modes for face recognition
face_recognition_modes = [recognize_faces, store_unknown_faces]

# Define sub-modes for object detection
object_detection_modes = [detect_objects, image_captioning]

def run_face_recognition(cap, lock, stop_event):
    mode = face_recognition_modes[current_sub_mode]
    audio_handler.add_audio_task("Starting-Facial-Recognition-Mode")
    mode(cap, lock, stop_event)

def run_object_detection(cap, lock, stop_event):
    mode = object_detection_modes[current_sub_mode]
    audio_handler.add_audio_task("Starting-Object-Detection-Mode")
    mode(cap, lock, stop_event, audio_handler)

def run_depth_sense(cap, lock, stop_event):
    audio_handler.add_audio_task("Starting-Depth-Sense-Mode")
    sense_depth(cap, lock, stop_event)

def run_ocr(cap, lock, stop_event):
    audio_handler.add_audio_task("Starting-Oh-See-are-Mode")
    perform_ocr(cap, lock, stop_event)

def run_sleep_mode(stop_event):
    audio_handler.add_audio_task("Entering-Sleep-Mode")
    while not stop_event.is_set():
        gc.collect()
        print("Garbage collected")
        time.sleep(10)
    audio_handler.add_audio_task("Exiting-Sleep-Mode")

def switch_module(module_number, cap, lock, stop_event):
    global active_threads, current_sub_mode
    stop_event.set()

    for thread in active_threads:
        thread.join()

    stop_event.clear()
    current_sub_mode = 0  # Reset sub-mode when switching main modes
    if module_number == 1:
        thread = threading.Thread(target=run_face_recognition, args=(cap, lock, stop_event))
    elif module_number == 2:
        thread = threading.Thread(target=run_object_detection, args=(cap, lock, stop_event))
    elif module_number == 3:
        thread = threading.Thread(target=run_depth_sense, args=(cap, lock, stop_event))
    elif module_number == 4:
        thread = threading.Thread(target=run_ocr, args=(cap, lock, stop_event))
    elif module_number == 5:
        thread = threading.Thread(target=run_sleep_mode, args=(stop_event,))
    else:
        print("Invalid module number.")
        return

    active_threads = [thread]
    thread.start()

def switch_sub_mode(increment, current_mode, cap, lock, stop_event):
    global current_sub_mode
    current_sub_mode += increment
    if current_mode == 1:
        current_sub_mode %= len(face_recognition_modes)
    elif current_mode == 2:
        current_sub_mode %= len(object_detection_modes)
    else:
        current_sub_mode = 0  # No sub-modes for other modes
    print(f"Switched to sub-mode {current_sub_mode}")
    switch_module(current_mode, cap, lock, stop_event)
