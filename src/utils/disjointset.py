from typing import Generic, TypeVar

T = TypeVar("T")


class DisjointSet(Generic[T]):
    def __init__(self) -> None:
        self._parents: dict[T, T] = {}
        self._sizes: dict[T, int] = {}

    def union(self, a: T, b: T) -> tuple[T, int]:
        a = self.find(a)
        b = self.find(b)

        if a == b:
            return a, self._sizes[a]

        if self._sizes[a] < self._sizes[b]:
            self._parents[a] = b
            self._sizes[b] += self._sizes[a]
            return b, self._sizes[b]
        else:
            self._parents[b] = a
            self._sizes[a] += self._sizes[b]
            return a, self._sizes[a]

    def find(self, a: T) -> T:
        if a not in self._parents:
            self._parents[a] = a
            self._sizes[a] = 1
            return a

        parent = self._parents[a]
        if parent == a:
            return a

        self._parents[a] = self.find(parent)
        return self._parents[a]

    def values(self) -> set[tuple[T, int]]:
        result = set()
        for elem in self._parents:
            result.add((elem, self._sizes[elem]))
        return result

    def __contains__(self, item: T) -> bool:
        return item in self._parents
