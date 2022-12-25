from __future__ import annotations

import argparse
import itertools
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.left: Point
        self.right: Point
        self.up: Point
        self.down: Point

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.x}, {self.y})"


def parse_input(s: str) -> tuple[Point, list[int | str]]:
    lines = list(itertools.takewhile(str.strip, s.splitlines()))
    longest = len(max(lines, key=len))
    map_ = [list(line.ljust(longest)) for line in lines]
    valid_points: dict[tuple[int, int], Point] = {}
    for x, row in enumerate(map_):
        for y, char in enumerate(row):
            if char == ".":
                valid_points[(x, y)] = Point(x, y)
    height, width = len(map_), longest
    for coord in valid_points:
        cur = coord
        while map_[(cur[0] + 1) % height][cur[1]] == " ":
            cur = ((cur[0] + 1) % height, cur[1])
        cur = ((cur[0] + 1) % height, cur[1])
        if map_[cur[0]][cur[1]] == "#":
            valid_points[coord].down = valid_points[coord]
        else:
            valid_points[coord].down = valid_points[cur]
        cur = coord
        while map_[(cur[0] - 1) % height][cur[1]] == " ":
            cur = ((cur[0] - 1) % height, cur[1])
        cur = ((cur[0] - 1) % height, cur[1])
        if map_[cur[0]][cur[1]] == "#":
            valid_points[coord].up = valid_points[coord]
        else:
            valid_points[coord].up = valid_points[cur]
        cur = coord
        while map_[cur[0]][(cur[1] + 1) % width] == " ":
            cur = (cur[0], (cur[1] + 1) % width)
        cur = (cur[0], (cur[1] + 1) % width)
        if map_[cur[0]][cur[1]] == "#":
            valid_points[coord].right = valid_points[coord]
        else:
            valid_points[coord].right = valid_points[cur]
        cur = coord
        while map_[cur[0]][(cur[1] - 1) % width] == " ":
            cur = (cur[0], (cur[1] - 1) % width)
        cur = (cur[0], (cur[1] - 1) % width)
        if map_[cur[0]][cur[1]] == "#":
            valid_points[coord].left = valid_points[coord]
        else:
            valid_points[coord].left = valid_points[cur]
    instructions: list[int | str] = list(
        map(
            lambda x: int(x) if x.isdigit() else x,
            filter(bool, re.split("([LR])", s.splitlines()[-1])),
        )
    )
    return valid_points[min(valid_points)], instructions


def compute(s: str) -> int:
    origin, instructions = parse_input(s)
    direction_dict = {
        "right": {"R": "down", "L": "up"},
        "down": {"R": "left", "L": "right"},
        "left": {"R": "up", "L": "down"},
        "up": {"R": "right", "L": "left"},
    }
    facing_values = {"right": 0, "down": 1, "left": 2, "up": 3}
    facing = "right"
    point = origin
    for instruction in instructions:
        if isinstance(instruction, int):
            for _ in range(instruction):
                point = getattr(point, facing)
        else:
            facing = direction_dict[facing][instruction]
    return 1000 * (point.x + 1) + 4 * (point.y + 1) + facing_values[facing]


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
