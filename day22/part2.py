from __future__ import annotations

import argparse
import itertools
import os.path
import re
from functools import lru_cache

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.left: tuple[Point, str]
        self.right: tuple[Point, str]
        self.up: tuple[Point, str]
        self.down: tuple[Point, str]

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"{type(self).__name__}({self.x}, {self.y})"


@lru_cache(maxsize=None)
def next_point(cur: tuple[int, int], direction: str) -> tuple[int, int, str]:
    nxt = None
    if 0 <= cur[0] < 50 and 49 < cur[1] < 100:
        if direction == "right":
            nxt = (cur[0], cur[1] + 1, "right")
        elif direction == "down":
            nxt = (cur[0] + 1, cur[1], "down")
        elif direction == "left":
            if cur[1] - 1 <= 49:
                nxt = (149 - cur[0], 0, "right")
            else:
                nxt = (cur[0], cur[1] - 1, "left")
        elif direction == "up":
            if cur[0] - 1 < 0:
                nxt = (cur[1] + 100, 0, "right")
            else:
                nxt = (cur[0] - 1, cur[1], "up")
    elif 0 <= cur[0] < 50 and 99 < cur[1] < 150:
        if direction == "right":
            if 150 <= cur[1] + 1:
                nxt = (149 - cur[0], 99, "left")
            else:
                nxt = (cur[0], cur[1] + 1, "right")
        elif direction == "down":
            if 50 <= cur[0] + 1:
                nxt = (cur[1] - 50, 99, "left")
            else:
                nxt = (cur[0] + 1, cur[1], "down")
        elif direction == "left":
            nxt = (cur[0], cur[1] - 1, "left")
        elif direction == "up":
            if cur[0] - 1 < 0:
                nxt = (199, cur[1] - 100, "up")
            else:
                nxt = (cur[0] - 1, cur[1], "up")
    elif 49 < cur[0] < 100 and 49 < cur[1] < 100:
        if direction == "right":
            if 100 <= cur[1] + 1:
                nxt = (49, cur[0] + 50, "up")
            else:
                nxt = (cur[0], cur[1] + 1, "right")
        elif direction == "down":
            nxt = (cur[0] + 1, cur[1], "down")
        elif direction == "left":
            if cur[1] - 1 <= 49:
                nxt = (100, cur[0] - 50, "down")
            else:
                nxt = (cur[0], cur[1] - 1, "left")
        elif direction == "up":
            nxt = (cur[0] - 1, cur[1], "up")
    elif 99 < cur[0] < 150 and 0 <= cur[1] < 50:
        if direction == "right":
            nxt = (cur[0], cur[1] + 1, "right")
        elif direction == "down":
            nxt = (cur[0] + 1, cur[1], "down")
        elif direction == "left":
            if cur[1] - 1 < 0:
                nxt = (149 - cur[0], 50, "right")
            else:
                nxt = (cur[0], cur[1] - 1, "left")
        elif direction == "up":
            if cur[0] - 1 <= 99:
                nxt = (cur[1] + 50, 50, "right")
            else:
                nxt = (cur[0] - 1, cur[1], "up")
    elif 99 < cur[0] < 150 and 49 < cur[1] < 100:
        if direction == "right":
            if 100 <= cur[1] + 1:
                nxt = (149 - cur[0], 149, "left")
            else:
                nxt = (cur[0], cur[1] + 1, "right")
        elif direction == "down":
            if 150 <= cur[0] + 1:
                nxt = (100 + cur[1], 49, "left")
            else:
                nxt = (cur[0] + 1, cur[1], "down")
        elif direction == "left":
            nxt = (cur[0], cur[1] - 1, "left")
        elif direction == "up":
            nxt = (cur[0] - 1, cur[1], "up")
    elif 149 < cur[0] < 200 and 0 <= cur[1] < 50:
        if direction == "right":
            if 50 <= cur[1] + 1:
                nxt = (149, cur[0] - 100, "up")
            else:
                nxt = (cur[0], cur[1] + 1, "right")
        elif direction == "down":
            if 200 <= cur[0] + 1:
                nxt = (0, cur[1] + 100, "down")
            else:
                nxt = (cur[0] + 1, cur[1], "down")
        elif direction == "left":
            if cur[1] - 1 < 0:
                nxt = (0, cur[0] - 100, "down")
            else:
                nxt = (cur[0], cur[1] - 1, "left")
        elif direction == "up":
            nxt = (cur[0] - 1, cur[1], "up")
    assert nxt is not None
    return nxt


def parse_input(s: str) -> tuple[Point, list[int | str]]:
    lines = list(itertools.takewhile(str.strip, s.splitlines()))
    longest = len(max(lines, key=len))
    map_ = [list(line.ljust(longest)) for line in lines]
    valid_points: dict[tuple[int, int], Point] = {}
    for x, row in enumerate(map_):
        for y, char in enumerate(row):
            if char == ".":
                valid_points[(x, y)] = Point(x, y)
    for coord in valid_points:
        cur = (*coord, "down")
        while map_[next_point(cur, cur[2])[0]][next_point(cur, cur[2])[1]] == " ":
            cur = next_point(cur, cur[2])
        cur = next_point(cur, cur[2])
        if map_[cur[0]][cur[1]] == "#":
            valid_points[coord].down = (valid_points[coord], "down")
        else:
            valid_points[coord].down = (valid_points[cur[:2]], cur[2])
        cur = (*coord, "up")
        while map_[next_point(cur, cur[2])[0]][next_point(cur, cur[2])[1]] == " ":
            cur = next_point(cur, cur[2])
        cur = next_point(cur, cur[2])
        if map_[cur[0]][cur[1]] == "#":
            valid_points[coord].up = (valid_points[coord], "up")
        else:
            valid_points[coord].up = (valid_points[cur[:2]], cur[2])
        cur = (*coord, "right")
        while map_[next_point(cur, cur[2])[0]][next_point(cur, cur[2])[1]] == " ":
            cur = next_point(cur, cur[2])
        cur = next_point(cur, cur[2])
        if map_[cur[0]][cur[1]] == "#":
            valid_points[coord].right = (valid_points[coord], "right")
        else:
            valid_points[coord].right = (valid_points[cur[:2]], cur[2])
        cur = (*coord, "left")
        while map_[next_point(cur, cur[2])[0]][next_point(cur, cur[2])[1]] == " ":
            cur = next_point(cur, cur[2])
        cur = next_point(cur, cur[2])
        if map_[cur[0]][cur[1]] == "#":
            valid_points[coord].left = (valid_points[coord], "left")
        else:
            valid_points[coord].left = (valid_points[cur[:2]], cur[2])
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
                point, facing = getattr(point, facing)
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
