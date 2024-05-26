# src/object_detection/object_detection.py

import time

def detect_objects(image, stop_event):
    print(f"Detecting objects in the image: {image}")
    for _ in range(10):  # Simulate 10 steps of processing
        if stop_event.is_set():
            print("Object detection stopped.")
            return
        time.sleep(2)  # Simulate processing time
    return ["object1", "object2"]
