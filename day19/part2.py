from __future__ import annotations

import argparse
import heapq
import os.path
import re
from collections.abc import Sequence
from typing import Any
from typing import Callable
from typing import NamedTuple
from typing import TYPE_CHECKING
from typing import TypeVar

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


class ResourceCounts(NamedTuple):
    ore: int = 1
    clay: int = 0
    obsidian: int = 0
    geode: int = 0


class Recipe(NamedTuple):
    ore: tuple[MineralCost, ...]
    clay: tuple[MineralCost, ...]
    obsidian: tuple[MineralCost, ...]
    geode: tuple[MineralCost, ...]


class State(NamedTuple):
    bot_counts: ResourceCounts
    mineral_counts: ResourceCounts


class QueueItem(NamedTuple):
    score: int
    time: int
    state: State


T = TypeVar("T", State, ResourceCounts, ResourceCounts)


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


@lru_cache(maxsize=None)
def can_build(recipe: Recipe, mineral_counts: ResourceCounts) -> tuple[str, ...]:
    return tuple(
        bot_type
        for bot_type in MINERALS
        if all(
            getattr(mineral_counts, mineral_cost.mineral) >= mineral_cost.cost
            for mineral_cost in getattr(recipe, bot_type)
        )
    )


@lru_cache(maxsize=None)
def limit_minerals(
    mineral_counts: ResourceCounts, limits: ResourceCounts
) -> ResourceCounts:
    return ResourceCounts(
        *(min(count, 2 * limit) for count, limit in zip(mineral_counts, limits))
    )


@lru_cache(maxsize=None)
def generate_states(state: State, recipe: Recipe, limits: ResourceCounts) -> set[State]:
    new_states = set()
    new_states.add(state)
    bots_to_consider = can_build(recipe, state.mineral_counts)
    if "geode" in bots_to_consider:
        bots_to_consider = ("geode",)
    for bot_type in bots_to_consider:
        if getattr(state.bot_counts, bot_type) > getattr(limits, bot_type):
            continue
        mineral_costs = getattr(recipe, bot_type)
        new_states.add(
            state._replace(
                mineral_counts=decrement(
                    state.mineral_counts,
                    *(mc.mineral for mc in mineral_costs),
                    amounts=tuple(mc.cost for mc in mineral_costs),
                ),
                bot_counts=increment(state.bot_counts, bot_type),
            )
        )
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


def compute(s: str) -> int:
    blueprints = []
    for line in s.splitlines():
        recipies = line.split("Each ")[1:]
        blueprints.append(
            Recipe(
                *(
                    tuple(
                        map(
                            lambda x: MineralCost(int(x.split()[0]), x.split()[1]),
                            re.findall(r"\d+ \w+", bot_recipe),
                        )
                    )
                    for bot_recipe in recipies
                )
            )
        )
    result = 1
    for i, recipe in enumerate(blueprints[:3], start=1):
        can_build.cache_clear()
        limit_minerals.cache_clear()
        generate_states.cache_clear()
        limits = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 10000000}
        for costs in recipe:
            for cost, mineral in costs:
                limits[mineral] = max(limits[mineral], cost)
        best = 0
        best_at_time = {i: 0 for i in range(32)}
        queue = [QueueItem(0, 0, State(ResourceCounts(), ResourceCounts()))]
        visited = set()
        while queue:
            queue_item = heapq.heappop(queue)
            state = queue_item.state
            best = max(best, state.mineral_counts.geode)
            best_at_time[queue_item.time] = min(
                best_at_time[queue_item.time], queue_item.score
            )
            if queue_item.time >= 31:
                continue
            if (
                queue_item.time < 23
                or queue_item.score <= best_at_time[queue_item.time] * 0.80
            ):
                new_states = generate_states(
                    state, recipe, ResourceCounts(*limits.values())
                )
                for new_state in new_states:
                    new_queue_item = queue_item._replace(
                        time=queue_item.time + 1,
                        score=-new_state.mineral_counts.geode,
                        state=new_state,
                    )
                    if new_queue_item not in visited:
                        heapq.heappush(queue, new_queue_item)
                        visited.add(new_queue_item)
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
