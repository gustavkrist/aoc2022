from __future__ import annotations

import argparse
import itertools
import os.path
from functools import lru_cache
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


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


def compute(s: str) -> int:
    points = frozenset(Point(*map(int, line.split(","))) for line in s.splitlines())
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


@pytest.mark.parametrize(
    ("input_s", "expected"),
    support.read_samples(SAMPLES, int, 2),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
