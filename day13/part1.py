from __future__ import annotations

import argparse
import os.path
from ast import literal_eval

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


PacketItem = int | list


def compare(left: PacketItem, right: PacketItem) -> bool:
    if isinstance(left, int) and isinstance(right, int):
        return left < right
    if isinstance(left, int) and isinstance(right, list):
        left = [left]
    if isinstance(left, list) and isinstance(right, int):
        right = [right]
    for l, r in zip(left, right):  # type: ignore # noqa: E741
        if l == r:
            continue
        return compare(l, r)
    return len(left) < len(right)  # type: ignore


def compute(s: str) -> int:
    return sum(
        i
        for i, pair in enumerate(s.split("\n\n"), start=1)
        if compare(*map(literal_eval, pair.rstrip().split("\n")))
    )


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
