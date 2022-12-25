from __future__ import annotations

import argparse
import math
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
collapsed_graph: Mapping[str, Mapping[str, int]]


def collapse_graph(
    graph: Mapping[str, set[str]], pressures: Mapping[str, int]
) -> Mapping[str, Mapping[str, int]]:
    new_graph: dict[str, dict[str, int]] = defaultdict(dict)
    for key in graph.keys():
        if not pressures[key] and key != "AA":
            continue
        distance = {k: math.inf for k in graph.keys()}
        distance[key] = 0
        queue = [key]
        while queue:
            valve = queue.pop(0)
            for neighbor in graph[valve]:
                if distance[neighbor] == math.inf:
                    queue.append(neighbor)
                    distance[neighbor] = distance[valve] + 1
                    if pressures[neighbor] or neighbor == "AA":
                        new_graph[key][neighbor] = int(distance[neighbor])
            new_graph[key][key] = int(distance[key])
    return new_graph


@lru_cache(maxsize=None)
def find_best(
    score: int, current_valve: str, current_time: int, closed_valves: frozenset[str]
) -> int:
    global collapsed_graph
    global pressures
    if current_time == 31:
        return score
    highest_score = score
    for valve in closed_valves:
        distance_to_valve = collapsed_graph[current_valve][valve]
        if current_time + distance_to_valve + 1 <= 30:
            pressure_from_valve = pressures[valve] * (30 - current_time - distance_to_valve)
            highest_score = max(
                highest_score,
                find_best(
                    score + pressure_from_valve,
                    valve,
                    current_time + distance_to_valve + 1,
                    closed_valves ^ {valve},
                ),
            )
    return highest_score


def compute(s: str) -> int:
    global graph
    global pressures
    graph = defaultdict(set)
    pressures = {}
    for line in s.splitlines():
        valves = re.findall("[A-Z]{2,}", line)
        pressure = re.findall(r"(?<==)\d+", line)[0]
        pressures[valves[0]] = int(pressure)
        graph[valves[0]] |= set(valves[1:])
    global collapsed_graph
    collapsed_graph = collapse_graph(graph, pressures)
    return find_best(0, "AA", 1, frozenset(k for k in collapsed_graph.keys()))


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
