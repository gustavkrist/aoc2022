from __future__ import annotations

import argparse
import os.path
import re
from collections import defaultdict
from collections.abc import Mapping
from functools import lru_cache

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")

graph: Mapping[str, set[str]]
pressures: Mapping[str, int]


@lru_cache(maxsize=None)
def increased_pressure(open: frozenset[str]) -> int:
    global pressures
    return sum(pressures[valve] for valve in open)


@lru_cache(maxsize=None)
def best_path(
    time: int,
    pressure: int,
    current_valve: str,
    open: frozenset[str],
) -> int:
    if time == 30:
        return pressure + increased_pressure(open)
    global graph
    global pressures
    permutations = []
    if current_valve not in open:
        permutations.append(
            (
                time + 1,
                pressure + increased_pressure(open),
                current_valve,
                open | {current_valve},
            )
        )
    for neighbor in graph[current_valve]:
        permutations.append(
            (
                time + 1,
                pressure + increased_pressure(open),
                neighbor,
                open,
            )
        )
    permutations.append(
        (
            time + 1,
            pressure + increased_pressure(open),
            current_valve,
            open,
        )
    )
    return max(best_path(*perm) for perm in permutations)


def compute(s: str) -> int:
    global graph
    graph = defaultdict(set)
    global pressures
    pressures = {}
    for line in s.splitlines():
        valves = re.findall("[A-Z]{2,}", line)
        pressure = re.findall(r"(?<==)\d+", line)[0]
        pressures[valves[0]] = int(pressure)
        graph[valves[0]] |= set(valves[1:])
    return best_path(1, 0, "AA", frozenset())


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
