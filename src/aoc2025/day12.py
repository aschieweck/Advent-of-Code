import sys
from pathlib import Path


class Present:
    def __init__(self, shape: list[list[bool]]) -> None:
        self.__shape = shape
        self.__area = sum([sum(row) for row in self.__shape])

    def __str__(self) -> str:
        result = []
        for row in self.__shape:
            line = ""
            for c in row:
                if c:
                    line += "#"
                else:
                    line += "."
            result.append(line)

        return "\n".join(result)

    def area(self) -> int:
        return self.__area

    @classmethod
    def parse(cls, shape_str: list[str]) -> "Present":
        shape = []
        for line in shape_str:
            row = [c == "#" for c in line]
            shape.append(row)
        return Present(shape)


class Region:
    def __init__(self, width: int, height: int, presents_requests: list[int]) -> None:
        self.__width = width
        self.__height = height
        self.__presents_requests = presents_requests

    def area(self) -> int:
        return self.__width * self.__height

    def get_presents_requested(self, idx: int) -> int:
        return self.__presents_requests[idx]

    def __str__(self) -> str:
        requests_str = [str(x) for x in self.__presents_requests]
        return f"{self.__width}x{self.__height}: {' '.join(requests_str)}"


def read_file(file_name: Path) -> tuple[list[Present], list[Region]]:
    presents = []
    regions = []
    with open(file_name) as f:
        content = f.read().splitlines()
        i = 0
        while i < len(content):
            key, value = content[i].split(":")
            if value:
                width, height = key.split("x")
                value = [int(x) for x in value.split()]
                regions.append(Region(int(width), int(height), value))
            else:
                shape = []
                i += 1
                while i < len(content) and content[i]:
                    shape.append(content[i])
                    i += 1
                presents.append(Present.parse(shape))

            i += 1

    return presents, regions


def simple_fittment_check(region: Region, presents: list[Present]) -> bool:
    space_needed = 0
    for i in range(0, len(presents)):
        space_needed += presents[i].area() * region.get_presents_requested(i)
    return space_needed <= region.area()


def check_present_fits(regions: list[Region], presents: list[Present]) -> int:
    count = 0
    for r in regions:
        if simple_fittment_check(r, presents):
            count += 1
    return count


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please provide the input file!", file=sys.stderr)
        exit(-1)

    presents, regions = read_file(Path(sys.argv[1]))
    count = check_present_fits(regions, presents)
    print(f"Phase 1: {count}")
