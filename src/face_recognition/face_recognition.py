# src/face_recognition/face_recognition.py

import time

def recognize_faces(image, stop_event):
    print(f"Recognizing faces in the image: {image}")
    for _ in range(10):  # Simulate 10 steps of processing
        if stop_event.is_set():
            print("Face recognition stopped.")
            return
        time.sleep(2)  # Simulate processing time
    return ["face1", "face2"]
