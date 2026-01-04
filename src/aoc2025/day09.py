import sys
from itertools import combinations, pairwise, chain
from pathlib import Path
from typing import NamedTuple, Final


class Point(NamedTuple):
    x: int
    y: int


class Line(NamedTuple):
    a: Point
    b: Point

    def is_horizontal(self) -> bool:
        return self.a.y == self.b.y

    def intersects(self, other: "Line") -> bool:
        self_horizontal: Final[bool] = self.is_horizontal()
        other_horizontal: Final[bool] = other.is_horizontal()

        if self_horizontal and other_horizontal:
            # Horizontal parallel and maybe touching
            return False

        elif not self_horizontal and not other_horizontal:
            # Vertical parallel and maybe touching
            return False

        return bool(
            self_horizontal
            and not other_horizontal
            and self.a.x <= other.a.x <= self.b.x
            and other.a.y <= self.a.y <= other.b.y
            or not self_horizontal
            and other_horizontal
            and other.a.x <= self.a.x <= other.b.x
            and self.a.y <= other.a.y <= self.b.y
        )


class Polygon:
    def __init__(self, corners: list[Point]) -> None:
        self.__corners: list[Point] = corners
        self.__horizontal_edges: set[Line] = set()
        self.__vertical_edges: set[Line] = set()
        self.__x_max: int = -1
        self.__y_max: int = -1

        self.__find_max()
        self.__create_edges()

    def __find_max(self) -> None:
        for corner in self.__corners:
            self.__x_max = max(self.__x_max, corner.x)
            self.__y_max = max(self.__y_max, corner.y)

    def __create_edges(self) -> None:
        tile_pairs = pairwise(chain(self.__corners, [self.__corners[0]]))
        for tile1, tile2 in tile_pairs:
            if tile1.x == tile2.x:
                start = Point(tile1.x, min(tile1.y, tile2.y))
                end = Point(tile1.x, max(tile1.y, tile2.y))
                self.__vertical_edges.add(Line(start, end))
            else:
                start = Point(min(tile1.x, tile2.x), tile1.y)
                end = Point(max(tile1.x, tile2.x), tile1.y)
                self.__horizontal_edges.add(Line(start, end))

    def is_rectangle_inside(self, rectangle: tuple[Point, ...]) -> bool:
        xs = [p.x for p in rectangle]
        ys = [p.y for p in rectangle]

        x_min = min(xs)
        x_max = max(xs)
        y_min = min(ys)
        y_max = max(ys)

        for corner in self.__corners:
            if x_min < corner.x < x_max and y_min < corner.y < y_max:
                return False

        for edge in self.__horizontal_edges:
            if y_min < edge.a.y < y_max and edge.a.x <= x_min and x_max <= edge.b.x:
                return False

        for edge in self.__vertical_edges:
            if x_min < edge.a.x < x_max and edge.a.y <= y_min and y_max <= edge.b.y:
                return False

        return True

    def __str__(self) -> str:
        result = []
        for y in range(0, self.__y_max + 2):
            row = []
            for x in range(0, self.__x_max + 3):
                row.append(".")
            result.append(row)

        for tile1, tile2 in self.__horizontal_edges:
            for x in range(tile1.x, tile2.x + 1):
                result[tile1.y][x] = "X"
        for tile1, tile2 in self.__vertical_edges:
            for y in range(tile1.y, tile2.y + 1):
                result[y][tile1.x] = "X"

        for corner in self.__corners:
            result[corner.y][corner.x] = "#"

        result = ("".join(x) for x in result)
        return "\n".join(result)


def read_file(file_name: Path) -> list[Point]:
    result = []
    with open(file_name) as f:
        for line in f.read().splitlines():
            x, y = line.split(",")
            result.append(Point(int(x), int(y)))
    return result


def get_biggest_rect(red_tiles: list[Point]) -> int:
    max_size = -1
    for tile1, tile2 in combinations(red_tiles, 2):
        a = abs(tile1.x - tile2.x) + 1
        b = abs(tile1.y - tile2.y) + 1
        size = a * b

        if size > max_size:
            max_size = size

    return max_size


def get_biggest_rect_2(red_tiles: list[Point], polygon: Polygon) -> int | None:
    candidates = []
    for tile1, tile2 in combinations(red_tiles, 2):
        a = abs(tile1.x - tile2.x) + 1
        b = abs(tile1.y - tile2.y) + 1
        size = a * b

        candidates.append((size, tile1, tile2))
    candidates.sort(reverse=True)

    for size, tile1, tile2 in candidates:
        rect = (Point(tile1.x, tile1.y), Point(tile1.x, tile2.y), Point(tile2.x, tile2.y), Point(tile2.x, tile1.y))
        if polygon.is_rectangle_inside(rect):
            return size

    return None


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please provide the input file!", file=sys.stderr)
        exit(-1)

    red_tiles = read_file(Path(sys.argv[1]))

    result = get_biggest_rect(red_tiles)
    print(f"Phase 1: {result}")

    polygon = Polygon(red_tiles)
    result = get_biggest_rect_2(red_tiles, polygon)
    print(f"Phase 2: {result}")
