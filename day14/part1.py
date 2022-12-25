from __future__ import annotations

import argparse
import os.path
from itertools import chain

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


def print_map(cave_map: list[list[str]]) -> None:
    for row in cave_map:
        print("".join([x or "." for x in row]))


def compute(s: str) -> int:
    all_points = [
        list(map(lambda x: tuple(map(int, x.split(","))), line.split(" -> ")))
        for line in s.splitlines()
    ]
    dimension_x = max(list(zip(*chain(*all_points)))[1])
    dimension_y_max = max(list(zip(*chain(*all_points)))[0])
    dimension_y_min = min(list(zip(*chain(*all_points)))[0])
    dimension_y = dimension_y_max - dimension_y_min + 1
    cave_map = [[''] * dimension_y for _ in range(dimension_x)]
    for row in all_points:
        for start, end in zip(row[:-1], row[1:]):
            if start[0] - end[0] < 0:
                for y in range(start[0], end[0] + 1):
                    cave_map[start[1] - 1][y - dimension_y_min] = "#"
            if start[0] - end[0] > 0:
                for y in range(end[0], start[0] + 1):
                    cave_map[start[1] - 1][y - dimension_y_min] = "#"
            if start[1] - end[1] < 0:
                for x in range(start[1], end[1] + 1):
                    cave_map[x - 1][start[0] - dimension_y_min] = "#"
            if start[1] - end[1] > 0:
                for x in range(end[1], start[1] + 1):
                    cave_map[x - 1][start[0] - dimension_y_min] = "#"
    while True:
        try:
            x = 0
            y = 500 - dimension_y_min
            while True:
                if y < 0 or y >= len(cave_map[0]):
                    break
                if not cave_map[x + 1][y]:
                    x += 1
                elif not cave_map[x + 1][y - 1]:
                    x += 1
                    y -= 1
                elif not cave_map[x + 1][y + 1]:
                    x += 1
                    y += 1
                else:
                    break
            if y < 0 or y >= len(cave_map[0]):
                break
            cave_map[x][y] = "o"
        except IndexError:
            break
    return str(list(chain(*cave_map))).count("o")


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
