from __future__ import annotations

import argparse
import os.path
import math
import heapq
from typing import Generator
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


def adjacent(x: int, y: int, height: int, width: int) -> Generator[tuple[int, int], None, None]:
    if x - 1 > 0:
        yield x - 1, y
    if y - 1 > 0:
        yield x, y - 1
    if x + 1 < height:
        yield x + 1, y
    if y + 1 < width:
        yield x, y + 1


def compute(s: str) -> int:
    graph = defaultdict(set)
    input_map = [list(line) for line in s.splitlines()]
    height, width = len(input_map), len(input_map[0])
    distances = {}
    visited = {}
    source = target = None
    for x, row in enumerate(input_map):
        for y, mark in enumerate(row):
            distances[(x, y)] = math.inf
            visited[(x, y)] = False
            for i, j in adjacent(x, y, height, width):
                if mark == 'S':
                    source = (x, y)
                    mark = 'a'
                if mark == 'E':
                    target = (x, y)
                    mark = 'z'
                if ord(mark) - ord(input_map[i][j]) >= -1:
                    graph[(x, y)].add((i, j))
    assert source is not None
    queue: list[tuple[int, tuple[int, int]]] = [(0, source)]
    while queue:
        distance, node = heapq.heappop(queue)
        if not visited[node]:
            visited[node] = True
            for neighbor in graph[node]:
                if distance + 1 < distances[neighbor]:
                    distances[neighbor] = distance + 1
                    heapq.heappush(queue, (distance + 1, neighbor))
    assert target is not None
    return int(distances[target])


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
