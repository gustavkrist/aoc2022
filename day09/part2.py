from __future__ import annotations

import argparse
import os.path
import enum

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


class Coordinate(tuple):
    def __add__(self, other):
        return Coordinate(v1 + v2 for v1, v2 in zip(self, other))

    def distance(self, other):
        return Coordinate(v1 - v2 for v1, v2 in zip(self, other))


class Direction(enum.Enum):
    UP = Coordinate((1, 0))
    DOWN = Coordinate((-1, 0))
    LEFT = Coordinate((0, -1))
    RIGHT = Coordinate((0, 1))

    def apply(self, other):
        return self.value + other


def compute(s: str) -> int:
    head = Coordinate((0, 0))
    tails = [Coordinate((0, 0))] * 9
    visited: set[Coordinate] = set()
    visited.add(tails[-1])
    for instruction in s.splitlines():
        direction, count = instruction.split()
        for _ in range(int(count)):
            if direction == 'U':
                head = Direction.UP.apply(head)
            elif direction == "D":
                head = Direction.DOWN.apply(head)
            elif direction == "L":
                head = Direction.LEFT.apply(head)
            elif direction == "R":
                head = Direction.RIGHT.apply(head)
            distance = head.distance(tails[0])
            if not (abs(distance[0]) < 2 and abs(distance[1]) < 2):
                if distance[0] > 0:
                    tails[0] = Direction.UP.apply(tails[0])
                elif distance[0] < 0:
                    tails[0] = Direction.DOWN.apply(tails[0])
                if distance[1] > 0:
                    tails[0] = Direction.RIGHT.apply(tails[0])
                elif distance[1] < 0:
                    tails[0] = Direction.LEFT.apply(tails[0])
            for front, behind in zip(range(8), range(1, 9)):
                distance = tails[front].distance(tails[behind])
                if not (abs(distance[0]) < 2 and abs(distance[1]) < 2):
                    if distance[0] > 0:
                        tails[behind] = Direction.UP.apply(tails[behind])
                    elif distance[0] < 0:
                        tails[behind] = Direction.DOWN.apply(tails[behind])
                    if distance[1] > 0:
                        tails[behind] = Direction.RIGHT.apply(tails[behind])
                    elif distance[1] < 0:
                        tails[behind] = Direction.LEFT.apply(tails[behind])
            visited.add(tails[-1])
    return sum(1 for _ in visited)


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
