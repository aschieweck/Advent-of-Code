import pytest
from pathlib import Path

from aoc2025.day04 import read_file, check_storage_location_safe, is_forkliftable, find_forkliftable_spots, remove_paper, clean_up_warehouse


TEST_FILE = Path(__file__).parent / "data" / "day04.txt"


@pytest.fixture
def warehouse() -> list[list[bool]]:
    return [
        [False, False, True, True, False, True, True, True, True, False],
        [True, True, True, False, True, False, True, False, True, True],
        [True, True, True, True, True, False, True, False, True, True],
        [True, False, True, True, True, True, False, False, True, False],
        [True, True, False, True, True, True, True, False, True, True],
        [False, True, True, True, True, True, True, True, False, True],
        [False, True, False, True, False, True, False, True, True, True],
        [True, False, True, True, True, False, True, True, True, True],
        [False, True, True, True, True, True, True, True, True, False],
        [True, False, True, False, True, True, True, False, True, False],
    ]


def test_read_file(warehouse):
    content = read_file(TEST_FILE)
    assert content == warehouse


@pytest.mark.parametrize("x,y,,expected",
                         [
                                (1, 1, True),
                                (5, 2, False),
                                (-1, 2, False),
                                (4, -1, False),
                                (10, 2, False),
                                (3, 10, False),
                         ])
def test_check_storage_location_safe(warehouse, x, y, expected):
    result = check_storage_location_safe(warehouse, x, y)
    assert result == expected


@pytest.mark.parametrize("x,y,,expected",
                         [
                                (6, 2, True),
                                (2, 0, True),
                                (3, 3, False),
                                (2, 4, False),
                                (0, 0, False),
                                (9, 9, False),
                         ])
def test_is_forkliftable(warehouse, x, y, expected):
    result = is_forkliftable(warehouse, x, y)
    assert result == expected


def test_find_forkliftable_spots(warehouse):
    result = find_forkliftable_spots(warehouse)
    expected = {
        (2, 0),
        (3, 0),
        (5, 0),
        (6, 0),
        (8, 0),
        (0, 1),
        (6, 2,),
        (0, 4),
        (9, 4),
        (0, 7),
        (0, 9),
        (2, 9),
        (8, 9),
    }

    assert len(result) == 13
    assert result == expected


def test_remove_paper(warehouse):
    remove_paper(warehouse, {(0, 0), (0, 9)})
    expected = [
        [False, False, True, True, False, True, True, True, True, False],
        [True, True, True, False, True, False, True, False, True, True],
        [True, True, True, True, True, False, True, False, True, True],
        [True, False, True, True, True, True, False, False, True, False],
        [True, True, False, True, True, True, True, False, True, True],
        [False, True, True, True, True, True, True, True, False, True],
        [False, True, False, True, False, True, False, True, True, True],
        [True, False, True, True, True, False, True, True, True, True],
        [False, True, True, True, True, True, True, True, True, False],
        [False, False, True, False, True, True, True, False, True, False],
    ]

    assert warehouse == expected


def test_clean_up_warehouse(warehouse):
    papers_removed = clean_up_warehouse(warehouse)
    expected = [
        [False, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, True, True, False, False, False, False],
        [False, False, False, True, True, True, True, False, False, False],
        [False, False, False, True, True, True, True, True, False, False],
        [False, False, False, True, False, True, False, True, True, False],
        [False, False, False, True, True, False, True, True, True, False],
        [False, False, False, True, True, True, True, True, False, False],
        [False, False, False, False, True, True, True, False, False, False]
    ]

    assert papers_removed == 43
    assert warehouse == expected
