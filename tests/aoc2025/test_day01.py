import sys
import os
print(f"\nDEBUG: CWD is {os.getcwd()}")
print(f"DEBUG: PYTHONPATH is {sys.path}")

import unittest
from pathlib import Path

from aoc2025.day01 import read_file, find_password, find_password_2


TEST_INPUT = [
    "L68",
    "L30",
    "R48",
    "L5",
    "R60",
    "L55",
    "L1",
    "L99",
    "R14",
    "L82",
]
TEST_FILE = Path(__file__).parent / "data" / "day01.txt"


class TestDay01(unittest.TestCase):

    def test_read_file(self):
        content = read_file(TEST_FILE)
        self.assertListEqual(content, TEST_INPUT)

    def test_phase1(self):
        password = find_password(TEST_INPUT)
        self.assertEqual(password, 3)

    def test_phase2(self):
        password = find_password_2(TEST_INPUT)
        self.assertEqual(password, 6)

    def test_integration(self):
        result = find_password(read_file(TEST_FILE))
        self.assertEqual(result, 3)

        result = find_password_2(read_file(TEST_FILE))
        self.assertEqual(result, 6)
