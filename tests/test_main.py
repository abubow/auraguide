# tests/test_main.py

import sys
import os
import unittest

# Add src directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.main import main

class TestMain(unittest.TestCase):
    def test_main(self):
        self.assertIsNone(main())

if __name__ == "__main__":
    unittest.main()