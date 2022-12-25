from __future__ import annotations

import argparse
import os.path
import operator
from ast import literal_eval
from math import prod
import itertools

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


PacketItem = int | list


def compare(left: PacketItem, right: PacketItem) -> bool:
    # match (left, right):
    #     case int(), int():
    #         return left < right
    #     case int(), list():
    #         left = [left]
    #     case list(), int():
    #         right = [right]
    if isinstance(left, int) and isinstance(right, int):
        return left < right
    if isinstance(left, int) and isinstance(right, list):
        left = [left]
    if isinstance(left, list) and isinstance(right, int):
        right = [right]
    assert isinstance(left, list) and isinstance(right, list)
    itertools.takewhile(operator.eq, iterator := iter(zip(left, right)))  # type: ignore[arg-type]
    return compare(*next(iterator, (len(left), len(right))))


def compute(s: str) -> int:
    return prod(map(lambda x: sum(x) + 1, zip(*[
            (compare(packet, [[2]]), compare(packet, [[6]]))
            for packet in map(literal_eval, filter(str.strip, f"{s}\n[[2]]".splitlines()))
    ])))


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
