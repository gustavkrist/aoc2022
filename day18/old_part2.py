from __future__ import annotations

import argparse
import os.path
from typing import Generator, NamedTuple
from tqdm import tqdm

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


def compute(s: str) -> int:
    points = list(Point(*map(int, line.split(","))) for line in s.splitlines())
    outer_edges = set()
    max_x = 0
    min_x = 100000
    max_y = 0
    min_y = 100000
    max_z = 0
    min_z = 100000
    for i, point1 in enumerate(points):
        max_x = max(max_x, point1.x)
        min_x = min(min_x, point1.x)
        max_y = max(max_y, point1.y)
        min_y = min(min_y, point1.y)
        max_z = max(max_z, point1.z)
        min_z = min(min_z, point1.z)
        for point2 in points[i:]:
            if point2 in set(point1.adjacent()):
                outer_edges.add((point1, point2))
    center = Point(
        *map(lambda x: x // 2, (max_x + min_x, max_y + min_y, max_z + min_z))
    )
    inner = [center]
    inner_edges = set()

    for point in inner:
        for adjacent in point.adjacent():
            if adjacent in points:
                continue
            if (
                adjacent in inner
                and (point, adjacent) not in inner_edges
                and (adjacent, point) not in inner_edges
            ):
                inner_edges.add((point, adjacent))
            elif adjacent not in inner:
                inner.append(adjacent)
                inner_edges.add((point, adjacent))

    breakpoint()

    for outer_point in tqdm(points):
        for adj in outer_point.adjacent():
            if adj not in points and adj not in inner:
                spreading = [adj]
                spreading_edges = set()
                for point in spreading:
                    for adjacent in point.adjacent():
                        if adjacent in points or adjacent in inner:
                            continue
                        if (
                            adjacent in spreading
                            and (point, adjacent) not in spreading_edges
                            and (adjacent, point) not in spreading_edges
                        ):
                            spreading_edges.add((point, adjacent))
                        elif adjacent not in spreading:
                            spreading.append(adjacent)
                            spreading_edges.add((point, adjacent))
                    if len(spreading) > 3:
                        break
                else:
                    inner.extend(spreading)
                    inner_edges |= spreading_edges

    return (len(points) - len(inner)) * 6 - 2 * (len(outer_edges) - len(inner_edges))


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
