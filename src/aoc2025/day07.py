import sys
import copy
from pathlib import Path
from typing import NewType


class ManifoldElement:
    pass


class BeamStart(ManifoldElement):
    def __str__(self) -> str:
        return "S"


class Beam(ManifoldElement):
    def __init__(self, value) -> None:
        self._value = value

    @property
    def value(self):
        return self._value

    def __add__(self, other: ManifoldElement | None) -> "Beam":
        if isinstance(other, Beam):
            return Beam(self._value + other._value)
        else:
            return Beam(self._value)

    def __str__(self) -> str:
        return "|"


class BeamSplitter(ManifoldElement):
    def __str__(self) -> str:
        return "^"


Manifold = NewType("Manifold", list[list[ManifoldElement | None]])


def read_file(file_name: Path) -> Manifold:
    manifold = Manifold([])
    with open(file_name) as f:
        for line in f.read().splitlines():
            manifold_line: list[ManifoldElement | None] = []
            for c in line:
                match c:
                    case "S":
                        manifold_line.append(BeamStart())
                    case "^":
                        manifold_line.append(BeamSplitter())
                    case ".":
                        manifold_line.append(None)
                    case _:
                        raise ValueError("Unknown Character in input")
            manifold.append(manifold_line)
    return manifold


def beam_tracer(manifold: Manifold) -> tuple[Manifold, int]:
    result_manifold = copy.deepcopy(manifold)
    split_count = 0
    for i in range(1, len(result_manifold)):
        for j in range(0, len(result_manifold[i])):
            last = result_manifold[i - 1][j]
            if isinstance(last, (BeamStart, Beam)):
                if isinstance(result_manifold[i][j], BeamSplitter):
                    result_manifold[i][j - 1] = Beam(1)
                    result_manifold[i][j + 1] = Beam(1)
                    split_count += 1
                else:
                    result_manifold[i][j] = Beam(1)

    return result_manifold, split_count


def quantum_beam_tracer(manifold: Manifold) -> tuple[Manifold, int]:
    result_manifold = copy.deepcopy(manifold)
    for i in range(1, len(result_manifold)):
        for j in range(0, len(result_manifold[i])):
            last = result_manifold[i - 1][j]
            current = result_manifold[i][j]
            if isinstance(last, BeamStart):
                result_manifold[i][j] = Beam(1)
            elif current is None:
                result_manifold[i][j] = copy.copy(last)

        for j in range(0, len(result_manifold[i])):
            last = result_manifold[i - 1][j]
            current= result_manifold[i][j]
            if isinstance(current, BeamSplitter) and isinstance(last, Beam):
                left = result_manifold[i][j - 1]
                result_manifold[i][j - 1] = last + left

                right = result_manifold[i][j + 1]
                result_manifold[i][j + 1] = last + right

    timelines_count = count_beams(result_manifold)
    return result_manifold, timelines_count


def count_beams(manifold: Manifold, line: int = -1) -> int:
    result = 0
    for elem in manifold[line]:
        if isinstance(elem, Beam):
            result += elem.value
    return result


def print_manifold(manifold: Manifold):
    for line in manifold:
        for elem in line:
            print(elem if elem else ".", end="")
        print()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please provide the input file!", file=sys.stderr)
        exit(-1)

    manifold = read_file(Path(sys.argv[1]))

    _, x = beam_tracer(manifold)
    print("Phase 1:", x)

    quatum_manifold, timelines_count = quantum_beam_tracer(manifold)
    print("Phase 2:", timelines_count)
