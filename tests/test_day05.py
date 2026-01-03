import pytest
from pathlib import Path

from aoc2025.day05 import (
    FreshIdRange,
    Ingredient,
    count_all_fresh_ingredients,
    find_fresh_ingredients,
    optimize_fresh_id_ranges,
    count_available_fresh_ingredients,
    read_file,
)


TEST_FILE = Path(__file__).parent / "data" / "day05.txt"


@pytest.fixture
def fresh_id_ranges() -> list[FreshIdRange]:
    return [FreshIdRange(3, 5), FreshIdRange(10, 14), FreshIdRange(16, 20), FreshIdRange(12, 18)]


@pytest.fixture
def optimized_fresh_id_ranges() -> list[FreshIdRange]:
    return [FreshIdRange(3, 5), FreshIdRange(10, 20)]


@pytest.fixture
def ingredients() -> list[Ingredient]:
    return [Ingredient(1), Ingredient(5), Ingredient(8), Ingredient(11), Ingredient(17), Ingredient(32)]


def test_read_file(fresh_id_ranges, ingredients):
    file_fresh_id_ranges, file_ingredients = read_file(TEST_FILE)
    assert file_fresh_id_ranges == fresh_id_ranges
    assert file_ingredients == ingredients


def test_optimize_fresh_id_db():
    fresh_id_ranges = [
        FreshIdRange(3, 6),
        FreshIdRange(2, 10),
    ]
    result = optimize_fresh_id_ranges(fresh_id_ranges)

    expected = [FreshIdRange(2, 10)]

    assert result == expected


def test_optimize_fresh_id_db_phase1(fresh_id_ranges, optimized_fresh_id_ranges):
    result = optimize_fresh_id_ranges(fresh_id_ranges)

    assert result == optimized_fresh_id_ranges


def test_find_fresh_ingredients():
    fresh_id_ranges = [FreshIdRange(3, 5), FreshIdRange(10, 20)]
    ingredients = [Ingredient(2), Ingredient(3), Ingredient(4), Ingredient(5), Ingredient(6)]

    fresh_ingredients = find_fresh_ingredients(fresh_id_ranges, ingredients)

    expected = [Ingredient(3), Ingredient(4), Ingredient(5)]

    assert expected == fresh_ingredients


def test_find_fresh_ingredients_phase1(fresh_id_ranges, ingredients):
    fresh_ingredients = find_fresh_ingredients(fresh_id_ranges, ingredients)

    expected = [Ingredient(5), Ingredient(11), Ingredient(17)]

    assert expected == fresh_ingredients


def test_coun_available_fresh_ingredients(optimized_fresh_id_ranges, ingredients):
    result = count_available_fresh_ingredients(optimized_fresh_id_ranges, ingredients)

    assert result == 3


def test_count_fresh_ingredients(optimized_fresh_id_ranges):
    result = count_all_fresh_ingredients(optimized_fresh_id_ranges)

    assert result == 14
