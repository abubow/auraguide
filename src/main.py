# src/main.py

from face_recognition.face_recognition import recognize_faces
from object_detection.object_detection import detect_objects

def main():
    image = "sample_image.jpg"
    faces = recognize_faces(image)
    objects = detect_objects(image)
    print(f"Faces: {faces}")
    print(f"Objects: {objects}")

if __name__ == "__main__":
    main()
