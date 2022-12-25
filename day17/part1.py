from __future__ import annotations

import argparse
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


Rock = tuple[complex, ...]


def print_tower(
    placed: set[complex], highest_rock: float, current_rock: Rock | None = None
) -> None:
    tower = [["."] * 7 for _ in range(int(highest_rock))]
    for point in placed:
        if point.imag > 0:
            tower[int(point.imag) - 1][int(point.real)] = "#"
    if current_rock:
        for point in current_rock:
            tower[int(point.imag) - 1][int(point.real)] = "@"
    print("\n".join(f'|{"".join(row)}|' for row in reversed(tower)) + "\n+-------+")


def up(rock: Rock, amount: int | float = 1) -> Rock:
    return tuple(point + amount * 1j for point in rock)


def down(rock: Rock) -> Rock:
    return tuple(point - 1j for point in rock)


def left(rock: Rock) -> Rock:
    new_rock = tuple(point - 1 for point in rock)
    if not all(point.real >= 0 for point in new_rock):
        return rock
    return new_rock


def right(rock: Rock) -> Rock:
    new_rock = tuple(point + 1 for point in rock)
    if not all(point.real <= 6 for point in new_rock):
        return rock
    return new_rock


def compute(s: str) -> int:
    rock_cycle = itertools.cycle(
        (
            tuple(i + 0j for i in range(2, 6)),
            (2 + 1j, 3 + 0j, 3 + 1j, 3 + 2j, 4 + 1j),
            (2 + 0j, 3 + 0j, 4 + 0j, 4 + 1j, 4 + 2j),
            tuple(2 + i * 1j for i in range(4)),
            (2 + 0j, 2 + 1j, 3 + 0j, 3 + 1j),
        )
    )
    move_cycle = itertools.cycle(s.rstrip())
    placed_rocks = {i + 0j for i in range(7)}
    highest_rock = 0.0
    for _ in range(2022):
        # breakpoint()
        rock = up(next(rock_cycle), 4 + highest_rock)
        new_rock = rock
        # print_tower(
        #     placed_rocks, max([highest_rock] + [p.imag for p in rock]), rock
        # )
        # breakpoint()
        # if i == 8:
        #     breakpoint()
        while not any(point in placed_rocks for point in new_rock):
            rock = new_rock
            # print_tower(
            #     placed_rocks, max([highest_rock] + [p.imag for p in rock]), rock
            # )
            # breakpoint()
            if next(move_cycle) == ">":
                new_rock = right(rock)
            else:
                new_rock = left(rock)
            if not any(point in placed_rocks for point in new_rock):
                rock = new_rock
            # print_tower(
            #     placed_rocks, max([highest_rock] + [p.imag for p in rock]), rock
            # )
            # breakpoint()
            new_rock = down(rock)
        for point in rock:
            placed_rocks.add(point)
        highest_rock = max([highest_rock] + [p.imag for p in rock])
        # print_tower(
        #     placed_rocks, max([highest_rock] + [p.imag for p in rock])
        # )
        # breakpoint()
    return int(highest_rock)


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
