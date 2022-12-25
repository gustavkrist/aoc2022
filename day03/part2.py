from __future__ import annotations

import argparse
import os.path
from functools import reduce
from string import ascii_letters

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


priority_dict = {k: v + 1 for v, k in enumerate(ascii_letters)}


def compute(s: str) -> int:
    lines = s.splitlines()
    return sum(
        priority_dict[next(iter(reduce(lambda x, y: x & y, map(set, group))))]  # type: ignore
        for group in zip(lines[::3], lines[1::3], lines[2::3])
    )
    # total = 0
    # lines = s.splitlines()
    # for i, j in zip(range(0, len(lines) + 1, 3), range(3, len(lines) + 1, 3)):
    #     total += priority_dict[next(iter(reduce(lambda x, y: x & y, map(set, lines[i:j]))))]  # type: ignore
    # return total


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
