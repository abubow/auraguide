# src/main.py

from face_recognition.face_recognition import recognize_faces
from object_detection.object_detection import detect_objects
from depth_sense.depth_sense import sense_depth
from ocr.ocr import perform_ocr

def main():
    image = "sample_image.jpg"
    faces = recognize_faces(image)
    objects = detect_objects(image)
    depth_data = sense_depth(image)
    ocr_text = perform_ocr(image)
    print(f"Faces: {faces}")
    print(f"Objects: {objects}")
    print(f"Depth Data: {depth_data}")
    print(f"OCR Text: {ocr_text}")

if __name__ == "__main__":
    main()
