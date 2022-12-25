from __future__ import annotations

import argparse
import heapq
import math
import os.path
import re
from collections import defaultdict, deque, namedtuple
from collections.abc import Mapping
from types import MappingProxyType
from typing import Any

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


def collapse_graph(
    graph: Mapping[str, set[str]], pressures: HashableMappingProxy
) -> HashableMappingProxy:
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
    return HashableMappingProxy(
        {k: HashableMappingProxy(v) for k, v in new_graph.items()}
    )


class State(namedtuple("State", "score,valve1,time1,valve2,time2,closed")):
    __slots__ = ()

    @property
    def time(self) -> int:
        return min(self.time1, self.time2)


class HashableMappingProxy:
    def __init__(self, m: dict[Any, Any]) -> None:
        self.m = MappingProxyType(m)

    def __hash__(self) -> int:
        if not hasattr(self, "_hash"):
            self._hash = hash(frozenset(self.items()))
        return self._hash

    def __getitem__(self, item: Any) -> Any:
        return self.m[item]

    def __setitem__(self, *_: Any) -> None:
        raise TypeError(
            "'HashableMappingProxy' object does not support item assignment"
        )

    def __getattr__(self, attr: str) -> Any:
        if attr == "__hash__":
            return self.__hash__
        return getattr(self.m, attr)


def new_human_states(
    pressures: HashableMappingProxy,
    distances: HashableMappingProxy,
    state: State,
) -> tuple[State, ...]:
    if state.time != state.time1:
        return (state,)
    if pressures[state.valve1] and state.valve1 in state.closed:
        return (
            state._replace(
                score=state.score - (30 - state.time) * pressures[state.valve1],
                time1=state.time1 + 1,
                closed=state.closed - {state.valve1},
            ),
        )
    new_states = []
    for neighbor in state.closed:
        new_states.append(
            state._replace(
                valve1=neighbor,
                time1=state.time1 + distances[state.valve1][neighbor],
            )
        )

    return tuple(new_states) or tuple([state._replace(time1=31)])


def new_elephant_states(
    pressures: HashableMappingProxy,
    distances: HashableMappingProxy,
    states: tuple[State, ...],
) -> tuple[State, ...]:
    new_states = []
    for state in states:
        if state.time != state.time2:
            new_states.append(state)
        elif pressures[state.valve2] and state.valve2 in state.closed:
            new_states.append(
                state._replace(
                    score=state.score - (30 - state.time) * pressures[state.valve2],
                    time2=state.time2 + 1,
                    closed=state.closed - {state.valve2},
                )
            )
        else:
            for neighbor in state.closed:
                new_states.append(
                    state._replace(
                        valve2=neighbor,
                        time2=state.time2 + distances[state.valve2][neighbor],
                    )
                )
    return tuple(new_states) or tuple([state._replace(time2=31) for state in states])


def compute(s: str) -> int:
    graph: dict[str, set[str]] = defaultdict(set)
    mutable_pressures = {}
    for line in s.splitlines():
        valves = re.findall("[A-Z]{2,}", line)
        pressure = re.findall(r"(?<==)\d+", line)[0]
        mutable_pressures[valves[0]] = int(pressure)
        graph[valves[0]] |= set(valves[1:])
    pressures = HashableMappingProxy(mutable_pressures)
    distances = collapse_graph(graph, pressures)
    non_zero_valves = frozenset(distances.keys()) - {"AA"}
    queue = [State(0, "AA", 5, "AA", 5, non_zero_valves)]
    best = 0
    best_for_time: dict[int, int] = defaultdict(int)
    # considered = set()
    while queue:
        state = heapq.heappop(queue)
        # considered.add(state)
        best = min(best, state.score)
        best_for_time[state.time] = min(best_for_time[state.time], state.score)
        if (
            state.time < 31
            and state.closed
            and (state.time < 17 or state.score <= 0.8 * best_for_time[state.time])
        ):
            # print(state.time, state.score, state.closed, best_for_time[state.time])
            human_states = new_human_states(pressures, distances, state)
            elephant_states = new_elephant_states(pressures, distances, human_states)
            for new_state in elephant_states:
                # if new_state not in considered:
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
