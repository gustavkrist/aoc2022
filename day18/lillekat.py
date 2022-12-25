from __future__ import annotations

import itertools
from functools import lru_cache
from typing import NamedTuple

from support import timing


class Point(NamedTuple):
    x: int
    y: int
    z: int


@lru_cache(maxsize=None)
def diagonals(point: Point) -> tuple[Point, ...]:
    return tuple(
        point._replace(
            x=point.x + x_direction,
            y=point.y + y_direction,
            z=point.z + z_direction,
        )
        for x_direction, y_direction in itertools.product((1, -1), repeat=2)
        for z_direction in (1, -1)
    )


@lru_cache(maxsize=None)
def adjacent(point: Point) -> tuple[Point, ...]:
    return tuple(
        point._replace(**{axis: getattr(point, axis) + direction})
        for axis in ("x", "y", "z")
        for direction in (1, -1)
    )


@lru_cache(maxsize=None)
def close_to_border(point: Point, points: frozenset[Point]) -> bool:
    return any(n in points for n in adjacent(point)) or any(
        any(nn in points for nn in adjacent(n)) for n in adjacent(point)
    )


def part1(points: frozenset[Point]) -> int:
    edgecount = 0
    visited = set()
    queue = [next(iter(points))]
    for point in queue:
        for adj in adjacent(point):
            if adj in points:
                if adj not in visited:
                    queue.append(adj)
                    visited.add(adj)
                edgecount += 1
        for diag in diagonals(point):
            if diag in points and diag not in visited:
                queue.append(diag)
                visited.add(diag)
    return len(points) * 6 - edgecount


def part2(points: frozenset[Point]) -> int:
    min_point = min(points)
    outside_point = min_point._replace(x=min_point.x - 1)
    queue = [outside_point]
    visited = {outside_point}
    perimeter = 0
    for point in queue:
        for adj in adjacent(point):
            if adj not in points and adj not in visited:
                if close_to_border(adj, points):
                    queue.append(adj)
                    visited.add(adj)
            elif adj in points:
                perimeter += 1
    return perimeter


def solve(s: str) -> tuple[int, int]:
    points = frozenset(Point(*map(int, line.split(","))) for line in s.splitlines())
    return part1(points), part2(points)


def main() -> int:
    with open(0) as f, timing():
        s = f.read().rstrip()
        print(solve(s))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
