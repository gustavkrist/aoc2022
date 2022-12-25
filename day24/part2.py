from __future__ import annotations

import argparse
import os
import os.path
import time
import curses
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


class Me(NamedTuple):
    x: int
    y: int


class Blizzard(NamedTuple):
    x: int
    y: int
    facing: str


def parse_input(s: str) -> tuple[int, int, frozenset[Blizzard]]:
    blizzards = set()
    direction_map = {"<": "left", "^": "up", ">": "right", "v": "down"}
    lines = s.splitlines()
    height, width = len(lines), len(lines[0])
    for x, line in enumerate(lines):
        for y, char in enumerate(line):
            if char not in (".", "#"):
                blizzards.add(Blizzard(x, y, direction_map[char]))
    return height, width, frozenset(blizzards)


T = TypeVar("T", Me, Blizzard)


@lru_cache(maxsize=None)
def move(
    thing: T,
    height: int | None = None,
    width: int | None = None,
    direction: str | None = None,
) -> T:
    direction_map = {
        "left": lambda x: x._replace(y=thing.y - 1),
        "up": lambda x: x._replace(x=thing.x - 1),
        "down": lambda x: x._replace(x=thing.x + 1),
        "right": lambda x: x._replace(y=thing.y + 1),
    }
    if isinstance(thing, Blizzard):
        assert height is not None and width is not None
        moved_thing = direction_map[thing.facing](thing)
        if moved_thing.x < 1:
            moved_thing = moved_thing._replace(x=height - 2)
        if moved_thing.x >= height - 1:
            moved_thing = moved_thing._replace(x=1)
        if moved_thing.y < 1:
            moved_thing = moved_thing._replace(y=width - 2)
        if moved_thing.y >= width - 1:
            moved_thing = moved_thing._replace(y=1)
    else:
        assert direction is not None
        moved_thing = direction_map[direction](thing)
    return moved_thing


@lru_cache(maxsize=None)
def move_blizzards(
    blizzards: frozenset[Blizzard], height: int, width: int
) -> frozenset[Blizzard]:
    return frozenset(move(blizzard, height, width) for blizzard in blizzards)


class State(NamedTuple):
    me: Me
    blizzards: frozenset[Blizzard]
    moves: int = 0


def print_state(state: State, height: int, width: int) -> str:
    lines = (
        [["#"] * width] + [["."] * width for _ in range(height - 2)] + [["#"] * width]
    )
    facing_map = {"left": "<", "up": "^", "down": "v", "right": ">"}
    for i in range(height):
        lines[i][0] = "#"
        lines[i][-1] = "#"
    for blizzard in state.blizzards:
        if lines[blizzard.x][blizzard.y] == ".":
            lines[blizzard.x][blizzard.y] = facing_map[blizzard.facing]
        elif lines[blizzard.x][blizzard.y].isdigit():
            lines[blizzard.x][blizzard.y] = str(int(lines[blizzard.x][blizzard.y]) + 1)
        else:
            lines[blizzard.x][blizzard.y] = "2"
    lines[0][1] = "."
    lines[height - 1][width - 2] = "."
    assert lines[state.me.x][state.me.y] == "."
    lines[state.me.x][state.me.y] = "E"
    output = f"Minute {state.moves}\n"
    output += "\n".join("".join(line) for line in lines)
    return output


@lru_cache(maxsize=None)
def get_invalid_points(blizzards: frozenset[Blizzard]) -> set[tuple[int, int]]:
    return {blizzard[:2] for blizzard in blizzards}


def print_traceback(
    graph: dict[State, State], state: State, height: int, width: int
) -> None:
    output = []
    while state != graph[state]:
        output.append(print_state(state, height, width))
        state = graph[state]

    def curses_debugger(stdscr: curses._CursesWindow) -> None:
        stdscr.clear()
        i = len(output) - 1
        stdscr.addstr(output[i])
        idx = output[i].index("E")
        y = output[i][:idx].count("\n")
        x = output[i].splitlines()[y].index("E")
        stdscr.addch(y, x, "E", curses.A_STANDOUT)
        stdscr.move(*map(lambda x: x - 1, stdscr.getmaxyx()))
        while True:
            key = stdscr.getkey()
            if key == "KEY_LEFT":
                i = min(i + 1, len(output) - 1)
            elif key == "KEY_RIGHT":
                i = max(i - 1, 0)
            elif key in ("", "q"):
                break
            else:
                continue
            stdscr.clear()
            stdscr.addstr(output[i])
            idx = output[i].index("E")
            y = output[i][:idx].count("\n")
            x = output[i].splitlines()[y].index("E")
            stdscr.addch(y, x, "E", curses.A_STANDOUT)
            stdscr.move(*map(lambda x: x - 1, stdscr.getmaxyx()))

    curses.wrapper(curses_debugger)


def compute(s: str) -> int:
    height, width, blizzards = parse_input(s)
    me = Me(0, 1)
    target = Me(height - 1, width - 2)
    queue = [State(me, blizzards)]
    visited = {State(me, blizzards)}
    state = None
    done = False

    graph = {State(me, blizzards): State(me, blizzards)}

    for state in queue:
        new_blizzards = move_blizzards(state.blizzards, height, width)
        invalid_points = get_invalid_points(new_blizzards)
        for direction in ("left", "down", "up", "right"):
            new_me = move(state.me, direction=direction)
            if new_me == target:
                # print_traceback(graph, state, height, width)
                new_state = state._replace(me=new_me)
                graph[new_state] = state
                state = new_state
                done = True
                break
            if (
                0 < new_me.x < height - 1
                and 0 < new_me.y < width - 1
                and new_me not in invalid_points
            ):
                new_state = state._replace(
                    me=new_me, blizzards=new_blizzards, moves=state.moves + 1
                )
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append(new_state)

                    graph[new_state] = state
        if done:
            break
        if state.me not in invalid_points:
            new_state = state._replace(
                me=state.me, blizzards=new_blizzards, moves=state.moves + 1
            )
            if new_state not in visited:
                visited.add(new_state)
                queue.append(new_state)

                graph[new_state] = state

    assert state is not None
    target = Me(0, 1)
    queue = [state]
    visited = {state}
    state = None
    done = False

    for state in queue:
        new_blizzards = move_blizzards(state.blizzards, height, width)
        invalid_points = get_invalid_points(new_blizzards)
        for direction in ("left", "down", "up", "right"):
            new_me = move(state.me, direction=direction)
            if new_me == target:
                # print_traceback(graph, state, height, width)
                new_state = state._replace(me=new_me)
                graph[new_state] = state
                state = new_state
                done = True
                break
            if (
                0 < new_me.x < height - 1
                and 0 < new_me.y < width - 1
                and new_me not in invalid_points
            ):
                new_state = state._replace(
                    me=new_me, blizzards=new_blizzards, moves=state.moves + 1
                )
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append(new_state)

                    graph[new_state] = state
        if done:
            break
        if state.me not in invalid_points:
            new_state = state._replace(
                me=state.me, blizzards=new_blizzards, moves=state.moves + 1
            )
            if new_state not in visited:
                visited.add(new_state)
                queue.append(new_state)

                graph[new_state] = state

    assert state is not None
    target = Me(height - 1, width - 2)
    queue = [state]
    visited = {state}
    state = None
    done = False

    for state in queue:
        new_blizzards = move_blizzards(state.blizzards, height, width)
        invalid_points = get_invalid_points(new_blizzards)
        for direction in ("left", "down", "up", "right"):
            new_me = move(state.me, direction=direction)
            if new_me == target:
                # print_traceback(graph, state, height, width)
                return state.moves + 1
            if (
                0 < new_me.x < height - 1
                and 0 < new_me.y < width - 1
                and new_me not in invalid_points
            ):
                new_state = state._replace(
                    me=new_me, blizzards=new_blizzards, moves=state.moves + 1
                )
                if new_state not in visited:
                    visited.add(new_state)
                    queue.append(new_state)

                    graph[new_state] = state
        if done:
            break
        if state.me not in invalid_points:
            new_state = state._replace(
                me=state.me, blizzards=new_blizzards, moves=state.moves + 1
            )
            if new_state not in visited:
                visited.add(new_state)
                queue.append(new_state)

                graph[new_state] = state
    return 0


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
