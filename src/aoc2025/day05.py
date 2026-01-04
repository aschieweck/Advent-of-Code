import sys
from pathlib import Path
from typing import NamedTuple, NewType


class FreshIdRange(NamedTuple):
    start: int
    end: int


Ingredient = NewType("Ingredient", int)


def read_file(file_name: Path) -> tuple[list[FreshIdRange], list[Ingredient]]:
    fresh_id_ranges = []
    ingredients = []

    with open(file_name) as f:
        is_reading_id_ranes = True
        for line in f.read().splitlines():
            if line == "":
                is_reading_id_ranes = False
            elif is_reading_id_ranes:
                id1, id2 = line.split("-")
                new_range = FreshIdRange(int(id1), int(id2))
                fresh_id_ranges.append(new_range)
            else:
                ingredients.append(int(line))

    return fresh_id_ranges, ingredients


def optimize_fresh_id_ranges(fresh_id_ranges: list[FreshIdRange]) -> list[FreshIdRange]:
    if len(fresh_id_ranges) == 0:
        return []

    fresh_id_ranges_sorted = sorted(fresh_id_ranges)

    optimized_fresh_id_ranges = [fresh_id_ranges_sorted[0]]
    for i in range(1, len(fresh_id_ranges_sorted)):
        current_range = optimized_fresh_id_ranges[-1]
        next_range = fresh_id_ranges_sorted[i]

        if current_range.end >= next_range.start:
            merged_end = max(current_range.end, next_range.end)
            optimized_fresh_id_ranges[-1] = FreshIdRange(current_range.start, merged_end)
        else:
            optimized_fresh_id_ranges.append(next_range)

    return optimized_fresh_id_ranges


def is_in_range(fresh_id_ranges: list[FreshIdRange], ingredient: Ingredient) -> bool:
    for id_range in fresh_id_ranges:
        if id_range.start <= ingredient <= id_range.end:
            return True

        if id_range.start > ingredient:
            return False

    return False


def find_fresh_ingredients(fresh_id_ranges: list[FreshIdRange], ingredients: list[Ingredient]) -> list[Ingredient]:
    return list(filter(lambda x: is_in_range(fresh_id_ranges, x), ingredients))


def count_available_fresh_ingredients(fresh_id_ranges: list[FreshIdRange], ingredients: list[Ingredient]) -> int:
    fresh_ingredients = find_fresh_ingredients(fresh_id_ranges, ingredients)
    return len(fresh_ingredients)


def count_all_fresh_ingredients(fresh_id_ranges: list[FreshIdRange]) -> int:
    result = 0
    for id_range in fresh_id_ranges:
        result += id_range.end - id_range.start + 1

    return result


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please provide the input file!", file=sys.stderr)
        exit(-1)

    fresh_id_ranges, ingredients = read_file(Path(sys.argv[1]))
    fresh_id_ranges = optimize_fresh_id_ranges(fresh_id_ranges)

    print("Phase 1:", count_available_fresh_ingredients(fresh_id_ranges, ingredients))
    print("Phase 2:", count_all_fresh_ingredients(fresh_id_ranges))
