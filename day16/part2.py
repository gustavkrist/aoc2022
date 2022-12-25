from __future__ import annotations

import argparse
import heapq
import math
import os.path
import re
from collections import defaultdict, deque
from collections.abc import Mapping
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


def collapse_graph(
    graph: Mapping[str, set[str]], pressures: Mapping[str, int]
) -> Mapping[str, dict[str, int]]:
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


@dataclass
class State:
    score: int
    valve1: str
    time1: int
    valve2: str
    time2: int
    closed: frozenset[str]

    @property
    def time(self) -> int:
        return min(self.time1, self.time2)

    def __lt__(self, other: object) -> bool:
        if isinstance(other, State):
            return self.score < other.score
        raise TypeError(
            f"'<' not supported between instances of 'State' and '{type(other)}'"
        )


def new_human_states(
    pressures: Mapping[str, int],
    distances: Mapping[str, dict[str, int]],
    state: State,
) -> list[State]:
    if state.time != state.time1:
        return [state]
    if pressures[state.valve1] and state.valve1 in state.closed:
        return [
            State(
                state.score - (29 - state.time) * pressures[state.valve1],
                state.valve1,
                state.time1 + 1,
                state.valve2,
                state.time2,
                state.closed - {state.valve1},
            )
        ]
    new_states = []
    for neighbor in state.closed:
        new_states.append(
            State(
                state.score,
                neighbor,
                state.time1 + distances[state.valve1][neighbor],
                state.valve2,
                state.time2,
                state.closed,
            )
        )

    return new_states or [
        State(state.score, state.valve1, 30, state.valve2, state.time2, state.closed)
    ]


def new_elephant_states(
    pressures: Mapping[str, int],
    distances: Mapping[str, Mapping[str, int]],
    states: list[State],
) -> list[State]:
    new_states = []
    for state in states:
        if state.time != state.time2:
            new_states.append(state)
        elif pressures[state.valve2] and state.closed:
            new_states.append(
                State(
                    state.score - (29 - state.time) * pressures[state.valve2],
                    state.valve1,
                    state.time1,
                    state.valve2,
                    state.time2 + 1,
                    state.closed - {state.valve2},
                )
            )
        else:
            for neighbor in state.closed:
                new_states.append(
                    State(
                        state.score,
                        state.valve1,
                        state.time1,
                        neighbor,
                        state.time2 + distances[state.valve2][neighbor],
                        state.closed,
                    )
                )
    return new_states or [
        State(state.score, state.valve1, state.time2, state.valve2, 30, state.closed)
        for state in states
    ]


def compute(s: str) -> int:
    graph: dict[str, set[str]] = defaultdict(set)
    pressures = {}
    for line in s.splitlines():
        valves = re.findall("[A-Z]{2,}", line)
        pressure = re.findall(r"(?<==)\d+", line)[0]
        pressures[valves[0]] = int(pressure)
        graph[valves[0]] |= set(valves[1:])
    distances = collapse_graph(graph, pressures)
    non_zero_valves = frozenset(distances.keys())
    queue = [State(0, "AA", 4, "AA", 4, non_zero_valves)]
    best = 0
    best_for_time: dict[int, int] = defaultdict(int)
    while queue:
        state = heapq.heappop(queue)
        best = min(best, state.score)
        best_for_time[state.time] = min(best_for_time[state.time], state.score)
        if (
            state.time < 30
            and state.closed
            and (state.time < 12 or state.score <= 0.8 * best_for_time[state.time])
        ):
            human_states = new_human_states(pressures, distances, state)
            elephant_states = new_elephant_states(pressures, distances, human_states)
            print(state.time, state.score, state.closed, best_for_time[state.time])
            for new_state in elephant_states:
                heapq.heappush(queue, new_state)
    return -best


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
