# src/ocr/ocr.py

import time

def perform_ocr(image, stop_event):
    print(f"Performing OCR on the image: {image}")
    for _ in range(10):  # Simulate 10 steps of processing
        if stop_event.is_set():
            print("OCR stopped.")
            return
        time.sleep(0.2)  # Simulate processing time
    return {"text": "sample_text"}
