from __future__ import annotations

import argparse
import collections
import itertools
import os.path
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


Rock = tuple[complex, ...]


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


class State(NamedTuple):
    rock_order: tuple[Rock, ...]
    move_order: str


class StateInfo(NamedTuple):
    cycle_start: int = 0
    height_at_start: float = 0.0


def compute(s: str) -> int:
    move_order = s.rstrip()
    iterations = 1_000_000_000_000
    rock_cycle = itertools.cycle(
        (
            tuple(i + 0j for i in range(2, 6)),
            (2 + 1j, 3 + 0j, 3 + 1j, 3 + 2j, 4 + 1j),
            (2 + 0j, 3 + 0j, 4 + 0j, 4 + 1j, 4 + 2j),
            tuple(2 + i * 1j for i in range(4)),
            (2 + 0j, 2 + 1j, 3 + 0j, 3 + 1j),
        )
    )
    move_cycle = itertools.cycle(move_order)
    placed_rocks = {i + 0j for i in range(7)}
    states: dict[State, StateInfo] = collections.defaultdict(StateInfo)
    highest_rock = 0.0
    for i in range(iterations):
        state = State(
            tuple(next(rock_cycle) for _ in range(5)),
            "".join(next(move_cycle) for _ in move_order),
        )
        if not states[state].cycle_start:
            states[state] = states[state]._replace(height_at_start=highest_rock)
            states[state] = states[state]._replace(cycle_start=i)
        elif (iterations - states[state].cycle_start) % (
            i - states[state].cycle_start
        ) == 0:
            total_height = states[state].height_at_start
            cycle_height = highest_rock - states[state].height_at_start
            cycle_start = states[state].cycle_start
            cycle_length = i - cycle_start
            total_height += cycle_height * (iterations - cycle_start) // cycle_length
            return int(total_height)
        rock = up(next(rock_cycle), 4 + highest_rock)
        new_rock = rock
        while not any(point in placed_rocks for point in new_rock):
            rock = new_rock
            if next(move_cycle) == ">":
                new_rock = right(rock)
            else:
                new_rock = left(rock)
            if not any(point in placed_rocks for point in new_rock):
                rock = new_rock
            new_rock = down(rock)
        for point in rock:
            placed_rocks.add(point)
        highest_rock = max([highest_rock] + [p.imag for p in rock])
    return int(highest_rock)


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
