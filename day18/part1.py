from __future__ import annotations

import argparse
import itertools
import os.path
from typing import Generator, NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


class Point(NamedTuple):
    x: int
    y: int
    z: int

    def adjacent(self) -> Generator[Point, None, None]:
        for axis in ("x", "y", "z"):
            for direction in (1, -1):
                yield self._replace(**{axis: getattr(self, axis) + direction})

    def diagonals(self) -> Generator[Point, None, None]:
        for x_direction, y_direction in itertools.product((1, -1), repeat=2):
            for z_direction in (1, -1):
                yield self._replace(
                    x=self.x + x_direction,
                    y=self.y + y_direction,
                    z=self.z + z_direction,
                )


def compute(s: str) -> int:
    points = {Point(*map(int, line.split(","))) for line in s.splitlines()}
    edgecount = 0
    visited = set()
    queue = [next(iter(points))]
    for point in queue:
        for adj in point.adjacent():
            if adj in points:
                if adj not in visited:
                    queue.append(adj)
                    visited.add(adj)
                edgecount += 1
        for diag in point.diagonals():
            if diag in points and diag not in visited:
                queue.append(diag)
                visited.add(diag)
    return len(points) * 6 - edgecount


@pytest.mark.parametrize(
    ("input_s", "expected"),
    support.read_samples(SAMPLES, int, 1),
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
