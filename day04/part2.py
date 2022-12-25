from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


def compute(s: str) -> int:
    return sum(
        1 if len(set1 & set2) > 0 else 0
        for line in s.splitlines()
        for set1, set2 in map(
            lambda x: (set(range(x[0], x[1] + 1)), set(range(x[2], x[3] + 1))),
            (list(map(int, line.replace("-", ",").split(","))),),
        )
    )
    # total = 0
    # for line in s.splitlines():
    #     elf1, elf2 = map(lambda x: x.split('-'), line.split(','))
    #     set1, set2 = map(lambda x: set(range(int(x[0]), int(x[1]) + 1)), [elf1, elf2])
    #     if len(set1 & set2) > 0:
    #         total += 1
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
