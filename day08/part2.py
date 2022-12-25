from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


def compute(s: str) -> int:
    trees = [tuple(map(int, line.rstrip())) for line in s.splitlines()]
    trees_t = tuple(zip(*trees))
    highest = 0
    height, width = len(trees), len(trees[0])
    for rownum, row in enumerate(trees):
        if rownum in [0, height - 1]:
            continue
        for colnum, tree in enumerate(row):
            if colnum in [0, width - 1]:
                continue
            left = right = up = down = 0
            for left, other_tree in enumerate(row[colnum - 1::-1], start=1):
                if tree <= other_tree:
                    break
            for right, other_tree in enumerate(row[colnum + 1:], start=1):
                if tree <= other_tree:
                    break
            for up, other_tree in enumerate(trees_t[colnum][rownum - 1::-1], start=1):
                if tree <= other_tree:
                    break
            for down, other_tree in enumerate(trees_t[colnum][rownum + 1:], start=1):
                if tree <= other_tree:
                    break
            total = left * right * up * down
            highest = max(total, highest)
    return highest


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
