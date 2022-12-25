from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


score_dict = {"A": 1, "B": 2, "C": 3}
win_dict = {'A': 'B', 'B': 'C', 'C': 'A'}
draw_dict = {'A': 'A', 'B': 'B', 'C': 'C'}
loss_dict = {'A': 'C', 'B': 'A', 'C': 'B'}


def compute(s: str) -> int:
    score = 0
    for line in s.rstrip().split("\n"):
        elf, outcome = line.split()
        if outcome == 'X':
            own = loss_dict[elf]
        elif outcome == 'Y':
            own = draw_dict[elf]
            score += 3
        else:
            own = win_dict[elf]
            score += 6
        score += score_dict[own]
    return score


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
