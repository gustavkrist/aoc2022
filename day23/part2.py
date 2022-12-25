from __future__ import annotations

import argparse
import os.path
from collections import Counter

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


def parse_input(s: str) -> set[complex]:
    return {
        x + y * 1j
        for x, line in enumerate(s.splitlines()[::-1])
        for y, char in enumerate(line)
        if char == "#"
    }


def consider_direction(
    point: complex, elves: set[complex], direction: str
) -> complex | None:
    if direction == "north" and all(
        p not in elves for p in (point + 1, point + 1 - 1j, point + 1 + 1j)
    ):
        return point + 1
    if direction == "south" and all(
        p not in elves for p in (point - 1, point - 1 - 1j, point - 1 + 1j)
    ):
        return point - 1
    if direction == "west" and all(
        p not in elves for p in (point - 1j, point - 1 - 1j, point + 1 - 1j)
    ):
        return point - 1j
    if direction == "east" and all(
        p not in elves for p in (point + 1j, point - 1 + 1j, point + 1 + 1j)
    ):
        return point + 1j
    return None


def consider_move(
    point: complex, elves: set[complex], moves: list[str]
) -> complex | None:
    if all(
        p not in elves
        for p in (
            point + 1,
            point - 1,
            point + 1j,
            point - 1j,
            point + 1 + 1j,
            point + 1 - 1j,
            point - 1 + 1j,
            point - 1 - 1j,
        )
    ):
        return None
    for move in moves:
        new_point = consider_direction(point, elves, move)
        if new_point is not None:
            return new_point
    return None


def calculate_area(elves: set[complex]) -> int:
    lowest_x = min(elves, key=lambda x: x.real).real
    highest_x = max(elves, key=lambda x: x.real).real
    lowest_y = min(elves, key=lambda x: x.imag).imag
    highest_y = max(elves, key=lambda x: x.imag).imag
    rect_area = (highest_x - lowest_x + 1) * (highest_y - lowest_y + 1)
    return int(rect_area) - len(elves)


def print_map(elves: set[complex]) -> None:
    highest_x = int(max(elves, key=lambda x: x.real).real)
    highest_y = int(max(elves, key=lambda x: x.imag).imag)
    map_ = [["."] * (highest_y + 1) for _ in range(highest_x + 1)]
    for elf in elves:
        map_[int(elf.real)][int(elf.imag)] = "#"
    for line in map_[::-1]:
        print("".join(line))


def compute(s: str) -> int:
    elves = parse_input(s)
    moves = ["north", "south", "west", "east"]
    new_elves = {elf for elf in elves}
    i = 0
    while elves != new_elves or i == 0:
        elves = new_elves
        new_elves = {elf for elf in elves}
        considered_moves_by_elf = {}
        considered_moves_count: dict[complex, int] = Counter()
        for elf in elves:
            new_pos = consider_move(elf, elves, moves)
            if new_pos is not None:
                considered_moves_by_elf[elf] = new_pos
                considered_moves_count[new_pos] += 1
        new_positions = {
            pos for pos, count in considered_moves_count.items() if count < 2
        }
        elves_to_move = {
            elf: pos
            for elf, pos in considered_moves_by_elf.items()
            if pos in new_positions
        }
        for elf, pos in elves_to_move.items():
            new_elves -= {elf}
            new_elves |= {pos}
        moves = moves[1:] + moves[:1]
        i += 1
    return i


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
