from __future__ import annotations

import argparse
import os.path
from copy import copy
from dataclasses import dataclass

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


@dataclass
class Number:
    val: int

    def __eq__(self, other: object) -> bool:
        return self is other

    def __repr__(self) -> str:
        return str(self.val)

    def __str__(self) -> str:
        return str(self.val)


def compute(s: str) -> int:
    numbers = list(map(lambda x: Number(int(x) * 811589153), s.splitlines()))
    process_order = copy(numbers)
    for _ in range(10):
        for number in process_order:
            if number.val == 0:
                continue
            idx = numbers.index(number)
            new_idx = idx + number.val
            new_idx %= len(numbers) - 1
            numbers.remove(number)
            numbers.insert(new_idx, number)
    zero = next(filter(lambda x: x.val == 0, numbers))
    zero_idx = numbers.index(zero)
    return sum(numbers[(zero_idx + i * 1000) % len(numbers)].val for i in range(1, 4))


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
