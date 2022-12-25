from __future__ import annotations

import argparse
import os.path
from tqdm import tqdm

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


def manhatten(start: complex, end: complex) -> int:
    return int(abs(start.real - end.real)) + int(abs(start.imag - end.imag))


def compute(s: str) -> int:
    cave_row = set()
    sensors = []
    beacons = []
    for line in s.splitlines():
        _, sensor_coords, beacon_coords = line.split("at ")
        sensor_coords, _, _ = sensor_coords.partition(":")
        sensor, beacon = tuple(
            map(
                lambda x: complex(*map(lambda y: int(y[2:]), x.split(", "))),
                [sensor_coords, beacon_coords],
            )
        )
        sensors.append(sensor)
        beacons.append(beacon)
    for sensor, beacon in zip(sensors, beacons):
        distance = manhatten(sensor, beacon)
        side_dist = distance - int(abs(2_000_000 - sensor.imag))
        if side_dist >= 0:
            for x in range(int(sensor.real) - side_dist, int(sensor.real) + side_dist + 1):
                point = (x + 2_000_000j)
                if point not in beacons:
                    cave_row.add(point)
    return len(cave_row)


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
