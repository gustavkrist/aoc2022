from __future__ import annotations

import argparse
import os.path
from itertools import chain
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


def print_map(cave_map: dict[complex, str], y_max: float) -> None:
    x_min = min(cave_map.keys(), key=lambda x: x.real).real
    x_max = max(cave_map.keys(), key=lambda x: x.real).real
    for y in range(int(y_max) + 2):
        print("".join(cave_map[complex(x, y)] or "." for x in range(int(x_min), int(x_max) + 1)))
    print("#" * int(x_max - x_min + 2))


def compute(s: str) -> int:
    all_points = [
        list(map(lambda x: complex(*map(int, x.split(","))), line.split(" -> ")))
        for line in s.splitlines()
    ]
    x_max = -10000.
    x_min = 10000.
    y_max = 0.
    cave_map: dict[complex, str] = defaultdict(str)
    for row in all_points:
        for start, end in zip(row[:-1], row[1:]):
            if (start - end).imag:
                if start.imag < end.imag:
                    y_max = max(y_max, end.imag)
                    iterable = range(int(start.imag), int(end.imag) + 1)
                else:
                    y_max = max(y_max, start.imag)
                    iterable = range(int(end.imag), int(start.imag) + 1)
                for y in iterable:
                    cave_map[complex(start.real, y)] = "#"
            else:
                if start.real < end.real:
                    x_min = min(x_min, start.real)
                    x_max = max(x_max, end.real)
                    iterable = range(int(start.real), int(end.real) + 1)
                else:
                    x_min = min(x_min, end.real)
                    x_max = max(x_max, start.real)
                    iterable = range(int(end.real), int(start.real) + 1)
                for x in iterable:
                    cave_map[complex(x, start.imag)] = "#"
    while not cave_map[500 + 0j]:
        point = 500 + 0j
        while True:
            if y_max + 1 <= point.imag:
                break
            if not cave_map[point + 1j]:
                point += 1j
            elif not cave_map[point - 1 + 1j]:
                point -= 1 - 1j
            elif not cave_map[point + 1 + 1j]:
                point += 1 + 1j
            else:
                break
        cave_map[point] = "o"
    return sum(1 for x in cave_map.values() if x == "o")


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
