import sys

Warehouse = list[list[bool]]


def read_file(file_name: str) -> Warehouse:
    warehouse = []
    with open(file_name) as f:
        for line in f.read().splitlines():
            storage_locations = [c == '@' for c in line]
            warehouse.append(storage_locations)

    return warehouse


def check_storage_location_safe(warehouse: Warehouse, x: int, y: int) -> bool:
    if 0 <= y < len(warehouse) and 0 <= x < len(warehouse[y]):
        return warehouse[y][x]

    return False


def is_forkliftable(warehouse: Warehouse, x: int, y: int) -> bool:
    if not check_storage_location_safe(warehouse, x, y):
        return False

    neighbours_coordinates = [
        (x + x_offset, y + y_offset)
        for x_offset in [-1, 0, 1] for y_offset in [-1, 0, 1]
        if not (x_offset == 0 and y_offset == 0)
    ]
    neighbours = [
        check_storage_location_safe(warehouse, neighbour_x, neighbour_y)
        for neighbour_x, neighbour_y in neighbours_coordinates
    ]

    return sum(neighbours) < 4


def find_forkliftable_spots(warehouse: Warehouse) -> set[tuple[int, int]]:
    spots = set()
    for y in range(0, len(warehouse)):
        for x in range(0, len(warehouse[y])):
            if is_forkliftable(warehouse, x, y):
                spots.add((x, y))

    return spots


def remove_paper(warehouse: Warehouse, spots: set[tuple[int, int]]):
    for (x, y) in spots:
        warehouse[y][x] = False


def clean_up_warehouse(warehouse: Warehouse) -> int:
    forkliftable_spots = find_forkliftable_spots(warehouse)
    papers_removed = len(forkliftable_spots)

    while len(forkliftable_spots) > 0:
        remove_paper(warehouse, forkliftable_spots)
        forkliftable_spots = find_forkliftable_spots(warehouse)
        papers_removed += len(forkliftable_spots)

    return papers_removed


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please provide the input file!", file=sys.stderr)
        exit(-1)

    warehouse = read_file(sys.argv[1])

    amount_of_forkliftable_spots = len(find_forkliftable_spots(warehouse))
    print("Phase 1:", amount_of_forkliftable_spots)

    papers_removed = clean_up_warehouse(warehouse)
    print("Phase 2:", papers_removed)
