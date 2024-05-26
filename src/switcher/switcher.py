# src/switcher/switcher.py

import threading
from face_recognition.face_recognition import recognize_faces
from object_detection.object_detection import detect_objects
from depth_sense.depth_sense import sense_depth
from ocr.ocr import perform_ocr

active_threads = []

def run_face_recognition(cap, lock, stop_event):
    recognize_faces(cap, lock, stop_event)

def run_object_detection(cap, lock, stop_event):
    detect_objects(cap, lock, stop_event)

def run_depth_sense(cap, lock, stop_event):
    sense_depth(cap, lock, stop_event)

def run_ocr(cap, lock, stop_event):
    perform_ocr(cap, lock, stop_event)

def switch_module(module_number, cap, lock, stop_event):
    global active_threads
    stop_event.set()

    for thread in active_threads:
        thread.join()

    stop_event.clear()
    if module_number == 1:
        thread = threading.Thread(target=run_face_recognition, args=(cap, lock, stop_event))
    elif module_number == 2:
        thread = threading.Thread(target=run_object_detection, args=(cap, lock, stop_event))
    elif module_number == 3:
        thread = threading.Thread(target=run_depth_sense, args=(cap, lock, stop_event))
    elif module_number == 4:
        thread = threading.Thread(target=run_ocr, args=(cap, lock, stop_event))
    else:
        print("Invalid module number.")
        return

    active_threads = [thread]
    thread.start()
