# tests/test_ocr.py

import unittest
from ocr.ocr import perform_ocr

class TestOCR(unittest.TestCase):
    def test_perform_ocr(self):
        result = perform_ocr("test_image.jpg")
        self.assertIsInstance(result, dict)

if __name__ == "__main__":
    unittest.main()
