from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass

from support import timing
from functools import partial


@dataclass
class Node:
    value: int
    left: Node | None = None
    right: Node | None = None

    def remove(self) -> None:
        self.left.right = self.right
        self.right.left = self.left

    def insert_after(self, node: Node) -> None:
        node.right = self.right
        node.right.left = node
        node.left = self
        self.right = node

    def insert_before(self, node: Node) -> None:
        node.left = self.left
        node.left.right = node
        node.right = self
        self.left = node

    def move(self, n: int, part: int = 1) -> None:
        multiplier = 811589153 if part == 2 else 1
        move = (self.value * multiplier) % n
        if self.value > 0:
            self.remove()
            node = self
            for _ in range(move):
                node = node.right
            node.insert_after(self)
        elif self.value < 0:
            self.remove()
            node = self
            for _ in range(abs(move)):
                node = node.left
            node.insert_before(self)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.value}, left={self.left.value}, right={self.right.value})"

    def __str__(self) -> str:
        return str(self.value)


def parse_input(s: str) -> list[Node]:
    nodes = list(map(lambda x: Node(int(x)), s.splitlines()))
    for left, right in zip(nodes[:-1], nodes[1:]):
        left.right = right
        right.left = left
    nodes[0].left = nodes[-1]
    nodes[-1].right = nodes[0]
    return nodes


def part1(nodes: list[Node]) -> int:
    n = len(nodes)
    for node in nodes:
        node.move(n)
    res = 0
    node = next(filter(lambda x: x.value == 0, nodes))
    for i in range(1, 3001):
        node = node.right
        if i % 1000 == 0:
            res += node.value
    return res


def part2(nodes: list[Node]) -> int:
    n = len(nodes)
    for _ in range(10):
        for node in nodes:
            node.move(n, part=2)
    res = 0
    node = next(filter(lambda x: x.value == 0, nodes))
    for i in range(1, 3001):
        node = node.right
        if i % 1000 == 0:
            res += node.value
    return res * 811589153


with open(0) as f, timing():
    s = f.read().rstrip()
    print(part1(parse_input(s)))
    nodes = parse_input(s)
    print(part2(list(nodes)))
