import sys
from math import sqrt
from pathlib import Path
from typing import NamedTuple

from utils.disjointset import DisjointSet


class JunctionBox(NamedTuple):
    x: int
    y: int
    z: int


class Connection(NamedTuple):
    distance: float
    junction_box_1: JunctionBox
    junction_box_2: JunctionBox


def read_file(file_name: Path) -> list[JunctionBox]:
    result = []
    with open(file_name) as f:
        for line in f.read().splitlines():
            x_str, y_str, z_str = line.split(",")
            result.append(JunctionBox(x=int(x_str), y=int(y_str), z=int(z_str)))
    return result


def calculate_distances(junction_boxes: list[JunctionBox]) -> list[Connection]:
    distances = []
    for i in range(0, len(junction_boxes)):
        for j in range(i + 1, len(junction_boxes)):
            junction_box1 = junction_boxes[i]
            junction_box2 = junction_boxes[j]
            x_diff = (junction_box1.x - junction_box2.x) ** 2
            y_diff = (junction_box1.y - junction_box2.y) ** 2
            z_diff = (junction_box1.z - junction_box2.z) ** 2
            distance = sqrt(x_diff + y_diff + z_diff)
            distances.append(Connection(distance=distance, junction_box_1=junction_box1, junction_box_2=junction_box2))

    return distances


def make_shortest_connections(
    connections: list[Connection], n: int
) -> tuple[DisjointSet[JunctionBox], list[Connection]]:
    disjoint_set = DisjointSet[JunctionBox]()

    results = []
    connections = sorted(connections)

    for i in range(0, n):
        candidate = connections[i]
        junction_box1 = candidate[1]
        junction_box2 = candidate[2]

        disjoint_set.union(junction_box1, junction_box2)
        results.append(candidate)

    return disjoint_set, results


def find_spanning_tree(
    junction_boxes: list[JunctionBox], connections: list[Connection]
) -> tuple[DisjointSet[JunctionBox], list[Connection]]:
    disjoint_set = DisjointSet()

    results = []
    connections = sorted(connections)
    for candidate in connections:
        junction_box1 = candidate[1]
        junction_box2 = candidate[2]

        parent1 = disjoint_set.find(junction_box1)
        parent2 = disjoint_set.find(junction_box2)

        if parent1 == parent2:
            continue

        _, circuit_size = disjoint_set.union(junction_box1, junction_box2)
        results.append(candidate)

        if circuit_size == len(junction_boxes):
            break

    return disjoint_set, results


def count_circuit_sizes(circuits: DisjointSet, n: int = 3):
    largest_circuits = sorted((x[1] for x in circuits.values()), reverse=True)[:n]
    result = 1
    for circuit in largest_circuits:
        result *= circuit
    return result


def phase2(connections: list[Connection]) -> int:
    last_connection = connections[-1]
    _, junction_box1, junction_box2 = last_connection

    return junction_box1.x * junction_box2.x


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the input file!", file=sys.stderr)
        print("And optionally the circuit size.", file=sys.stderr)
        exit(-1)

    junction_boxes = read_file(Path(sys.argv[1]))
    connection_count = int(sys.argv[2]) if len(sys.argv) == 3 else 10

    connections = calculate_distances(junction_boxes)

    circuits, _ = make_shortest_connections(connections, connection_count)
    largest_circuits_sizes = count_circuit_sizes(circuits, 3)
    print(f"Phase 1: {largest_circuits_sizes}")

    _, spanning_tree = find_spanning_tree(junction_boxes, connections)
    x = phase2(spanning_tree)
    print(f"Phase 2: {x}")
