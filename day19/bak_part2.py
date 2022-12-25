from __future__ import annotations

import argparse
import itertools
import operator
import os.path
import re
from collections import deque
from collections.abc import Sequence
from pprint import pprint
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Callable, NamedTuple, TypeVar

if TYPE_CHECKING:
    F = TypeVar("F", bound=Callable[..., Any])

    def lru_cache(maxsize: None) -> Callable[[F], F]:
        def _wrapper(f: F) -> F:
            return f

        return _wrapper

else:
    from functools import lru_cache

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


MINERALS = ("ore", "clay", "obsidian", "geode")


class MineralCost(NamedTuple):
    cost: int
    mineral: str


class RobotCounts(NamedTuple):
    ore: int = 1
    clay: int = 0
    obsidian: int = 0
    geode: int = 0


class MineralCounts(NamedTuple):
    ore: int = 1
    clay: int = 0
    obsidian: int = 0
    geode: int = 0


class State(NamedTuple):
    time: int
    bot_counts: RobotCounts
    mineral_counts: MineralCounts


T = TypeVar("T", State, RobotCounts, MineralCounts)


@lru_cache(maxsize=None)
def increment(tup: T, *fields: str, amounts: Sequence[int] = (1,)) -> T:
    return tup._replace(
        **{
            field: getattr(tup, field) + amount
            for field, amount in zip(fields, amounts)
        }
    )


@lru_cache(maxsize=None)
def decrement(tup: T, *fields: str, amounts: Sequence[int] = (1,)) -> T:
    return tup._replace(
        **{
            field: getattr(tup, field) - amount
            for field, amount in zip(fields, amounts)
        }
    )


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

    def __repr__(self) -> str:
        return repr(self.m)

    def __str__(self) -> str:
        return str(self.m)


Recipe = HashableMappingProxy


@lru_cache(maxsize=None)
def can_build(recipe: Recipe, mineral_counts: MineralCounts) -> tuple[str, ...]:
    return tuple(
        bot_type
        for bot_type in MINERALS
        if all(
            getattr(mineral_counts, mineral_cost.mineral) >= mineral_cost.cost
            for mineral_cost in recipe[bot_type]
        )
    )


@lru_cache(maxsize=None)
def limit_minerals(
    mineral_counts: MineralCounts, limits: MineralCounts
) -> MineralCounts:
    return MineralCounts(
        *(min(count, 2 * limit) for count, limit in zip(mineral_counts, limits))
    )


def generate_states(state: State, recipe: Recipe, limits: MineralCounts) -> set[State]:
    state = increment(state, "time")
    new_states = set()
    new_states.add(state)
    bots_to_consider = can_build(recipe, state.mineral_counts)
    if "geode_bot" in bots_to_consider:
        bots_to_consider = ("geode_bot",)
    for bot_type in bots_to_consider:
        if getattr(state.bot_counts, bot_type) > getattr(limits, bot_type):
            continue
        mineral_costs = recipe[bot_type]
        new_mineral_counts = decrement(
            state.mineral_counts,
            *(mc.mineral for mc in mineral_costs),
            amounts=tuple(mc.cost for mc in mineral_costs),
        )
        new_bot_counts = increment(state.bot_counts, bot_type.removesuffix("_bot"))
        new_state = state._replace(
            mineral_counts=new_mineral_counts, bot_counts=new_bot_counts
        )
        new_states.add(new_state)
    return set(
        map(
            lambda x: x._replace(
                mineral_counts=limit_minerals(
                    increment(
                        x.mineral_counts,
                        *MINERALS,
                        amounts=tuple(
                            getattr(state.bot_counts, mineral) for mineral in MINERALS
                        ),
                    ),
                    limits,
                )
            ),
            new_states,
        )
    )


def print_debug_trace(states: Sequence[State], recipe: Recipe) -> None:
    print(
        "== Minute 1 ==\n1 ore-collecting robot collects 1 ore; you now have 1 ore.\n"
    )
    for prev_state, state in zip(states[:-1], states[1:]):
        print(f"== Minute {state.time + 1} ==")
        bot_type = None
        robot_count = 0
        bot_difference = tuple(
            itertools.starmap(
                operator.sub, zip(state.bot_counts, prev_state.bot_counts)
            )
        )
        if any(bot_difference):
            bot_type = MINERALS[bot_difference.index(1)]
            mineral_costs = recipe[bot_type]
            an = "an" if bot_type == "obsidian" else "a"
            collecting = "collecting" if bot_type != "geode" else "cracking"
            print(
                f"Spend {' and '.join(map(lambda x: ' '.join(map(str, x)), mineral_costs))} to start building {an} {bot_type}-{collecting} robot."
            )
        mineral_increases = {
            mineral: getattr(prev_state.bot_counts, mineral) for mineral in MINERALS
        }
        for mineral, increase in mineral_increases.items():
            if increase:
                robot_count = getattr(prev_state.bot_counts, mineral)
                s = "s" if robot_count > 1 else ""
                collecting = "collecting" if mineral != "geode" else "cracking"
                collect = "collect" if mineral != "geode" else "crack"
                mineral_count = getattr(state.mineral_counts, mineral)
                geode_s1 = "s" if mineral == "geode" and increase > 1 else ""
                geode_s2 = "s" if mineral == "geode" and mineral_count > 1 else ""
                open_geode = "open " if mineral == "geode" else ""
                print(
                    f"{robot_count} {mineral}-{collecting} robot{s} {collect}{'' if s else 's'} {increase} {mineral}{geode_s1}; you now have {mineral_count} {open_geode}{mineral}{geode_s2}."
                )
        if bot_type is not None:
            collecting = "collecting" if bot_type != "geode" else "cracking"
            print(
                f"The new {bot_type}-{collecting} robot is ready; you now have {getattr(state.bot_counts, bot_type)} of them."
            )
        print()


def compute(s: str) -> int:
    blueprints = []
    for line in s.splitlines():
        bot_costs = {}
        recipies = line.split("Each ")[1:]
        for bot_recipe, bot_type in zip(recipies, MINERALS):
            mineral_costs = tuple(
                map(
                    lambda x: MineralCost(int(x.split()[0]), x.split()[1]),
                    re.findall(r"\d+ \w+", bot_recipe),
                )
            )
            bot_costs[bot_type] = mineral_costs
        blueprints.append(HashableMappingProxy(bot_costs))
    result = 1
    for i, recipe in enumerate(blueprints[:3], start=1):
        can_build.cache_clear()
        limit_minerals.cache_clear()
        # print(f"{i / len(blueprints):.2%}")
        print(f"{i / 3:.2%}")
        # graph = {
        #     State(0, RobotCounts(), MineralCounts()): State(
        #         0, RobotCounts(), MineralCounts()
        #     )
        # }

        limits = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 10000000}
        for costs in recipe.values():
            for cost, mineral in costs:
                limits[mineral] = max(limits[mineral], cost)
        best = 0
        queue = deque([State(0, RobotCounts(), MineralCounts())])
        visited = set()
        while queue:
            state = queue.popleft()
            print(state.time)
            best = max(best, state.mineral_counts.geode)
            if state.time > 23 and not state.mineral_counts.geode:
                continue
            if state.time < 31:
                new_states = generate_states(
                    state, recipe, MineralCounts(*limits.values())
                )
                for new_state in new_states:
                    if new_state not in visited:
                        queue.append(new_state)
                        visited.add(new_state)

                        # graph[new_state] = state

        # best_state = max(visited, key=lambda x: x.mineral_counts.geode)
        # states = [best_state]
        # state = best_state
        # while graph.get(state) != state:
        #     state = graph[state]
        #     states.append(state)
        # pprint(recipe.m)
        # print_debug_trace(tuple(reversed(states)), recipe)
        result *= best
    return result


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
