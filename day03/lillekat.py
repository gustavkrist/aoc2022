from functools import reduce
from string import ascii_letters

priority_dict = {k: v + 1 for v, k in enumerate(ascii_letters)}


def part1(input: str) -> int:
    return sum(
        priority_dict[
            next(iter(set(line[: len(line) // 2]) & set(line[len(line) // 2 :])))
        ]
        for line in input.splitlines()
    )


def part2(input: str) -> int:
    lines = input.splitlines()
    return sum(
        priority_dict[next(iter(reduce(lambda x, y: x & y, map(set, group))))]
        for group in zip(lines[::3], lines[1::3], lines[2::3])
    )
