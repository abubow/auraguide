# tests/test_face_recognition.py

import unittest
from src.face_recognition.face_recognition import recognize_faces

class TestFaceRecognition(unittest.TestCase):
    def test_recognize_faces(self):
        result = recognize_faces("test_image.jpg")
        self.assertIsInstance(result, list)

if __name__ == "__main__":
    unittest.main()