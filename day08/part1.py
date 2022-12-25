from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


def compute(s: str) -> int:
    trees = [tuple(map(int, line.rstrip())) for line in s.splitlines()]
    counted = [[False] * len(row) for row in trees]
    width, height = len(trees[0]), len(trees)
    for i, row in enumerate(trees):
        if i in (0, height - 1):
            continue
        tallest = -1
        for j, tree in enumerate(row):
            if tallest == 9:
                break
            if tree > tallest:
                tallest = tree
                if not counted[i][j]:
                    counted[i][j] = True
        tallest = -1
        for j, tree in enumerate(row[::-1]):
            if tallest == 9:
                break
            if tree > tallest:
                tallest = tree
                if not counted[i][-(j + 1)]:
                    counted[i][-(j + 1)] = True
    counted_t: list[list[bool]] = list(map(list, zip(*counted)))
    for i, col in enumerate(zip(*trees)):
        if i in (0, width - 1):
            continue
        tallest = -1
        for j, tree in enumerate(col):
            if tallest == 9:
                break
            if tree > tallest:
                tallest = tree
                if not counted_t[i][j]:
                    counted_t[i][j] = True
        tallest = -1
        for j, tree in enumerate(col[::-1]):
            if tallest == 9:
                break
            if tree > tallest:
                tallest = tree
                if not counted_t[i][-(j + 1)]:
                    counted_t[i][-(j + 1)] = True
    return sum(map(sum, counted_t)) + 4


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
