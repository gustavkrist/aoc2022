from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


def parse_input(s: str) -> int:
    number_dict = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
    total = 0
    for line in s.splitlines():
        num = 0
        for pow, char in enumerate(line[::-1]):
            num += (5 ** pow) * number_dict[char]
        total += num
    return total


def compute(s: str) -> int:
    print(parse_input(s))
    return 0


@pytest.mark.parametrize(
    ("input_s", "expected"),
    support.read_samples(SAMPLES, str, 1),
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
