from __future__ import annotations

import argparse
import os.path
from typing import Generator, cast

import pytest
import sympy

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


def manhatten(start: tuple[int, int], end: tuple[int, int]) -> int:
    return int(abs(start[0] - end[0])) + int(abs(start[1] - end[1]))


def Adjacent(point: tuple[int, int], max_width: int, max_height: int) -> Generator[tuple[int, int], None, None]:
    x, y = point
    if x > 0:
        yield x - 1, y
    if x <= max_width:
        yield x + 1, y
    if y > 0:
        yield x, y - 1
    if y <= max_height:
        yield x, y + 1


def compute_intersection(
    sensor1: tuple[tuple[int, int], int], sensor2: tuple[tuple[int, int], int]
) -> set[tuple[int, int]]:
    if manhatten(sensor1[0], sensor2[0]) > max(sensor1[1], sensor2[1]):
        return set()
    sensor1_lines = (
        sympy.Segment(
            sympy.Point(sensor1[0][0], sensor1[0][1] - sensor1[1]),
            sympy.Point(sensor1[0][0] + sensor1[1], sensor1[0][1]),
        ),
        sympy.Segment(
            sympy.Point(sensor1[0][0], sensor1[0][1] + sensor1[1]),
            sympy.Point(sensor1[0][0] + sensor1[1], sensor1[0][1]),
        ),
        sympy.Segment(
            sympy.Point(sensor1[0][0] - sensor1[1], sensor1[0][1]),
            sympy.Point(sensor1[0][0], sensor1[0][1] + sensor1[1]),
        ),
        sympy.Segment(
            sympy.Point(sensor1[0][0] - sensor1[1], sensor1[0][1]),
            sympy.Point(sensor1[0][0], sensor1[0][1] - sensor1[1]),
        ),
    )
    sensor2_lines = (
        sympy.Segment(
            sympy.Point(sensor2[0][0], sensor2[0][1] - sensor2[1]),
            sympy.Point(sensor2[0][0] + sensor2[1], sensor2[0][1]),
        ),
        sympy.Segment(
            sympy.Point(sensor2[0][0], sensor2[0][1] + sensor2[1]),
            sympy.Point(sensor2[0][0] + sensor2[1], sensor2[0][1]),
        ),
        sympy.Segment(
            sympy.Point(sensor2[0][0] - sensor2[1], sensor2[0][1]),
            sympy.Point(sensor2[0][0], sensor2[0][1] + sensor2[1]),
        ),
        sympy.Segment(
            sympy.Point(sensor2[0][0] - sensor2[1], sensor2[0][1]),
            sympy.Point(sensor2[0][0], sensor2[0][1] - sensor2[1]),
        ),
    )
    intersection_points = set()
    for l1 in sensor1_lines:
        for l2 in sensor2_lines:
            intersection = l1.intersect(l2)
            if intersection and isinstance(intersection, sympy.FiniteSet):
                intersection_points.add(tuple(map(int, tuple(tuple(intersection)[0]))))
    return intersection_points  # type: ignore


def compute(s: str) -> int:
    sensors = []
    beacons = []
    for line in s.splitlines():
        _, sensor_coords, beacon_coords = line.split("at ")
        sensor_coords, _, _ = sensor_coords.partition(":")
        sensor, beacon = cast(
            tuple[tuple[int, int], tuple[int, int]],
            tuple(
                map(
                    lambda x: tuple(map(lambda y: int(y[2:]), x.split(", "))),
                    [sensor_coords, beacon_coords],
                )
            ),
        )
        distance = manhatten(sensor, beacon)
        sensors.append((sensor, distance))
        beacons.append(beacon)

    intersection_points = set()

    for sensor1 in sensors:
        for sensor2 in sensors:
            if sensor1 != sensor2:
                intersections = compute_intersection(sensor1, sensor2)
                if intersections:
                    intersection_points |= intersections
    for intersection in intersection_points:
        for adjacent in Adjacent(intersection, 4_000_000, 4_000_000):
            if all(manhatten(sensor[0], adjacent) > sensor[1] for sensor in sensors):
                if 0 <= adjacent[0] <= 4_000_000 and 0 <= adjacent[1] <= 4_000_000:
                    return adjacent[0] * 4_000_000 + adjacent[1]
    return 0


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
