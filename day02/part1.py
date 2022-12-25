from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


score_dict = {"A": 1, "B": 2, "C": 3}


def compute(s: str) -> int:
    score = 0
    for line in s.rstrip().split("\n"):
        elf, own = line.split()
        own = chr(ord(own) - 23)
        if elf == own:
            score += 3
        elif (
            (elf == "A" and own == "B")
            or (elf == "B" and own == "C")
            or (elf == "C" and own == "A")
        ):
            score += 6
        score += score_dict[own]
    return score


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
