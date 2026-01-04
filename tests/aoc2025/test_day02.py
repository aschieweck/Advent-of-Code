import unittest
from pathlib import Path

from aoc2025.day02 import read_file, check_ids, check_ids_regex, check_ids_2, check_ids_2_regex


TEST_INPUT = [
    (11, 22),
    (95, 115),
    (998, 1012),
    (1188511880, 1188511890),
    (222220, 222224),
    (1698522, 1698528),
    (446443, 446449),
    (38593856, 38593862),
    (565653, 565659),
    (824824821, 824824827),
    (2121212118, 2121212124),
]
TEST_FILE = Path(__file__).parent / "data" / "day02.txt"


class TestDay02(unittest.TestCase):

    def test_read_file(self):
        content = read_file(TEST_FILE)
        self.assertListEqual(content, TEST_INPUT)

    def test_phase1(self):
        for func in [check_ids, check_ids_regex]:
            test_cases = [
                (TEST_INPUT[0], 11 + 22),
                (TEST_INPUT[1], 99),
                (TEST_INPUT[2], 1010),
                (TEST_INPUT[3], 1188511885),
                (TEST_INPUT[4], 222222),
                (TEST_INPUT[5], 0),
                (TEST_INPUT[6], 446446),
                (TEST_INPUT[7], 38593859),
                (TEST_INPUT[8], 0),
                (TEST_INPUT[9], 0),
                (TEST_INPUT[10], 0),
            ]
            for data, expected in test_cases:
                with self.subTest(data=data):
                    result = func([data])
                    self.assertEqual(result, expected)

            password = func(TEST_INPUT)
            self.assertEqual(password, 1227775554)

    def test_phase2(self):
        for func in [check_ids_2, check_ids_2_regex]:
            test_cases = [
                (TEST_INPUT[0], 11 + 22),
                (TEST_INPUT[1], 99 + 111),
                (TEST_INPUT[2], 999 + 1010),
                (TEST_INPUT[3], 1188511885),
                (TEST_INPUT[4], 222222),
                (TEST_INPUT[5], 0),
                (TEST_INPUT[6], 446446),
                (TEST_INPUT[7], 38593859),
                (TEST_INPUT[8], 565656),
                (TEST_INPUT[9], 824824824),
                (TEST_INPUT[10], 2121212121),
            ]
            for data, expected in test_cases:
                with self.subTest(data=data):
                    result = func([data])
                    self.assertEqual(result, expected)

            password = func(TEST_INPUT)
            self.assertEqual(password, 4174379265)

    def test_integration(self):
        result = check_ids(read_file(TEST_FILE))
        self.assertEqual(result, 1227775554)
        result = check_ids_regex(read_file(TEST_FILE))
        self.assertEqual(result, 1227775554)

        result = check_ids_2(read_file(TEST_FILE))
        self.assertEqual(result, 4174379265)
        result = check_ids_2_regex(read_file(TEST_FILE))
        self.assertEqual(result, 4174379265)
