# tests/test_object_detection.py

import unittest
from src.object_detection.object_detection import detect_objects

class TestObjectDetection(unittest.TestCase):
    def test_detect_objects(self):
        result = detect_objects("test_image.jpg")
        self.assertIsInstance(result, list)

if __name__ == "__main__":
    unittest.main()
