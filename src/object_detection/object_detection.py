# src/object_detection/object_detection.py

import time
import cv2
import torch
from ultralytics import YOLO
import os
from collections import defaultdict
from datetime import datetime, timedelta
def load_model():
    model_path = 'yolov10b.pt'
    if not os.path.exists(model_path):
        print("Downloading YOLOv10 model weights...")
        torch.hub.download_url_to_file('https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov10b.pt', model_path)
    model = YOLO(model_path)
    return model

# Initialize the object detection model
model = load_model()
COCO_CLASSES = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light",
    "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
    "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
    "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
    "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch",
    "potted plant", "bed", "dining table", "toilet", "TV", "laptop", "mouse", "remote", "keyboard",
    "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase",
    "scissors", "teddy bear", "hair drier", "toothbrush"
]

# Map these class names to the model
model_class_names = {i: name for i, name in enumerate(COCO_CLASSES)}

def detect_objects(cap, lock, stop_event, audio_handler, threshold=4, interval=5):
    window_name = "Object Detection"
    cv2.namedWindow(window_name)
    object_positions = defaultdict(list)
    start_time = datetime.now()

    while not stop_event.is_set():
        with lock:
            ret, image = cap.read()
            if not ret:
                break

        # Perform object detection
        results = model.predict(image)

        # Extract bounding boxes and labels
        boxes = results[0].boxes  # Assuming results[0] is the first (and only) result
        detected_objects = []
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())
            label = f"{model_class_names.get(cls, 'Unknown')} {conf:.2f}"
            detected_objects.append((model_class_names.get(cls, 'Unknown'), (x1 + x2) / 2))  # Store object name and its horizontal position
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Update the object positions
        for obj_name, x_pos in detected_objects:
            object_positions[obj_name].append(x_pos)

        # Check if the interval has passed
        current_time = datetime.now()
        if (current_time - start_time).seconds >= interval:
            # Calculate the average position for each object
            avg_positions = {obj: sum(positions) / len(positions) for obj, positions in object_positions.items()}

            # Sort the objects by their average horizontal position
            sorted_objects = sorted(avg_positions.items(), key=lambda x: x[1])

            # Trigger audio if the count of any object exceeds the threshold
            for obj, _ in sorted_objects:
                if len(object_positions[obj]) >= threshold:
                    audio_handler.add_audio_task(f"objects/{obj}")

            # Reset the object positions and start time
            object_positions.clear()
            start_time = current_time

        # Display the resulting frame
        if image is not None:
            cv2.imshow(window_name, image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_event.set()
            break
    cv2.destroyWindow(window_name)
    print("Object Detection Stopped.")

def image_captioning(cap, lock, stop_event, audio_handler):
    window_name = "Image Captioning"
    cv2.namedWindow(window_name)
    while not stop_event.is_set():
        with lock:
            ret, image = cap.read()
            if not ret:
                break
        if image is not None:
            cv2.imshow(window_name, image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_event.set()
            break
        time.sleep(0.2)  # Simulate some processing time
    cv2.destroyWindow(window_name)
    print("Image Captioning Stopped.")