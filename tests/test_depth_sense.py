# tests/test_depth_sense.py

import unittest
from src.depth_sense.depth_sense import sense_depth

class TestDepthSense(unittest.TestCase):
    def test_sense_depth(self):
        result = sense_depth("test_image.jpg")
        self.assertIsInstance(result, dict)

if __name__ == "__main__":
    unittest.main()