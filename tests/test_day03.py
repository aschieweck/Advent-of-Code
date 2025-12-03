import unittest
from pathlib import Path

from aoc2025.day03 import read_file, max_joltage


TEST_INPUT = [
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1, 1],
    [8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9],
    [2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 3, 4, 2, 7, 8],
    [8, 1, 8, 1, 8, 1, 9, 1, 1, 1, 1, 2, 1, 1, 1],
]
TEST_FILE = Path(__file__).parent / "data" / "day03.txt"


class TestDay03(unittest.TestCase):

    def test_read_file(self):
        content = read_file(TEST_FILE)
        self.assertListEqual(content, TEST_INPUT)

    def test_phase1(self):
        test_cases = [
            (TEST_INPUT[0], 98),
            (TEST_INPUT[1], 89),
            (TEST_INPUT[2], 78),
            (TEST_INPUT[3], 92),
        ]
        for data, expected in test_cases:
            with self.subTest(data=data):
                result = max_joltage([data])
                self.assertEqual(result, expected)

        jolatge = max_joltage(TEST_INPUT)
        self.assertEqual(jolatge, 357)

    def test_phase2(self):
        test_cases = [
            (TEST_INPUT[0], 987654321111),
            (TEST_INPUT[1], 811111111119),
            (TEST_INPUT[2], 434234234278),
            (TEST_INPUT[3], 888911112111),
        ]
        for data, expected in test_cases:
            with self.subTest(data=data):
                result = max_joltage([data], 12)
                self.assertEqual(result, expected)

        jolatge = max_joltage(TEST_INPUT, 12)
        self.assertEqual(jolatge, 3121910778619)

    def test_integration(self):
        result = max_joltage(read_file(TEST_FILE), 2)
        self.assertEqual(result, 357)

        result = max_joltage(read_file(TEST_FILE), 12)
        self.assertEqual(result, 3121910778619)
