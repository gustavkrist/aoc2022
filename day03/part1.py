from __future__ import annotations

import argparse
import os.path
from string import ascii_letters

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


priority_dict = {k: v + 1 for v, k in enumerate(ascii_letters)}


def compute(s: str) -> int:
    return sum(
        priority_dict[
            next(iter(set(line[: len(line) // 2]) & set(line[len(line) // 2 :])))
        ]
        for line in s.splitlines()
    )
    # total = 0
    # for line in s.splitlines():
    #     splitpoint = len(line) // 2
    #     total += priority_dict[next(iter(set(line[:splitpoint]) & set(line[splitpoint:])))]
    # return total


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
