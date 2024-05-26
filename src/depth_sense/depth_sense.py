# src/depth_sense/depth_sense.py

import time

def sense_depth(image, stop_event):
    print(f"Sensing depth in the image: {image}")
    for _ in range(10):  # Simulate 10 steps of processing
        if stop_event.is_set():
            print("Depth sensing stopped.")
            return
        time.sleep(0.2)  # Simulate processing time
    return {"depth": "sample_depth_data"}
