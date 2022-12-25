from __future__ import annotations

import argparse
import os.path
from collections import deque

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


def compute(s: str) -> str:
    crate_lines = []
    lines = iter(s.splitlines())
    for line in lines:
        if not line.rstrip():
            break
        crate_lines.append(line.rstrip())
    crates: list[deque[str]] = [deque() for _ in range(int(crate_lines.pop()[-1]))]
    for line in crate_lines:
        for crate, letter in enumerate(range(1, len(line) + 1, 4)):
            if line[letter] != ' ':
                crates[crate].appendleft(line[letter])
    for instruction in lines:
        count, source, target = map(int, instruction.split()[1::2])
        for _ in range(count):
            if crates[source - 1]:
                crates[target - 1].append(crates[source - 1].pop())
    return ''.join(map(lambda x: '' if not x else x[-1], crates))


@pytest.mark.parametrize(
    ("input_s", "expected"),
    support.read_samples(SAMPLES, str, 1),
)
def test(input_s: str, expected: str) -> None:
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
