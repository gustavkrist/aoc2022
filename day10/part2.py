from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


def draw_pixel(image: list[list[str]], x: int, cycle: int) -> None:
    pixel = '#' if cycle % 40 in (x - 1, x, x + 1) else '.'
    image[cycle // 40][cycle % 40] = pixel


def compute(s: str) -> int:
    cycle = 0
    x = 1
    image = [[' '] * 40 for _ in range(6)]
    for instruction in s.splitlines():
        draw_pixel(image, x, cycle)
        if len(instruction.split()) > 1:
            amount = int(instruction.split()[1])
            cycle += 1
            draw_pixel(image, x, cycle)
            x += amount
        cycle += 1
    print('\n'.join(''.join(line) for line in image))
    return 0


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
