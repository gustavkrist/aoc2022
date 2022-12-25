from __future__ import annotations

import operator
import re
from functools import lru_cache
from typing import Callable, NamedTuple

import support


class Monkey(NamedTuple):
    value: int | X | None
    operator: Callable[[int | X, int | X], int] | None
    dependencies: tuple[str, str] | None


class X:
    def __init__(self) -> None:
        self.operations: list[Callable[[int], int]] = []

    def __add__(self, other: int) -> X:
        self.operations.append(lambda x: operator.sub(x, other))
        return self

    def __radd__(self, other: int) -> X:
        self.operations.append(lambda x: operator.sub(x, other))
        return self

    def __sub__(self, other: int) -> X:
        self.operations.append(lambda x: operator.add(x, other))
        return self

    def __rsub__(self, other: int) -> X:
        self.operations.append(lambda x: operator.sub(other, x))
        return self

    def __mul__(self, other: int) -> X:
        self.operations.append(lambda x: operator.floordiv(x, other))
        return self

    def __rmul__(self, other: int) -> X:
        self.operations.append(lambda x: operator.floordiv(x, other))
        return self

    def __floordiv__(self, other: int) -> X:
        self.operations.append(lambda x: operator.mul(x, other))
        return self

    def __rfloordiv__(self, other: int) -> X:
        self.operations.append(lambda x: operator.floordiv(other, x))
        return self


def parse_input(s: str) -> dict[str, Monkey]:
    troop = {}
    pat = re.compile(r" ([\+\-\*/]) ")
    operators = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.floordiv,
    }
    for line in s.splitlines():
        monkey, _, rest = line.partition(": ")
        if rest.isnumeric():
            troop[monkey] = Monkey(int(rest), None, None)
        else:
            dep1, op, dep2 = pat.split(rest)
            troop[monkey] = Monkey(None, operators[op], (dep1, dep2))
    return troop


def part1(troop: dict[str, Monkey]) -> int:
    @lru_cache(maxsize=None)
    def find_root(monkey: Monkey) -> int:
        if monkey.value is not None:
            assert isinstance(monkey.value, int)
            return monkey.value
        assert monkey.dependencies is not None and monkey.operator is not None
        return monkey.operator(*map(lambda x: find_root(troop[x]), monkey.dependencies))

    return find_root(troop["root"])


def part2(troop: dict[str, Monkey]) -> int:
    @lru_cache(maxsize=None)
    def find_value(monkey: Monkey) -> int | X:
        if monkey.value is not None:
            return monkey.value
        assert monkey.dependencies is not None and monkey.operator is not None
        return monkey.operator(
            *map(lambda x: find_value(troop[x]), monkey.dependencies)
        )

    troop['humn'] = Monkey(X(), None, None)
    assert troop["root"].dependencies is not None
    left = find_value(troop[troop["root"].dependencies[0]])
    right = find_value(troop[troop["root"].dependencies[1]])

    if isinstance(left, X):
        assert isinstance(right, int)
        for op in left.operations[::-1]:
            right = op(right)
        return right
    else:
        assert isinstance(left, int) and isinstance(right, X)
        for op in right.operations[::-1]:
            left = op(left)
        return left


def main() -> int:
    with open(0) as f, support.timing():
        monkeys = parse_input(f.read().rstrip())
        print(part1(monkeys))
        print(part2(monkeys))
    return 0


if __name__ == "__main__":
    main()
