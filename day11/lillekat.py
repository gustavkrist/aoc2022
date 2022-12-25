from __future__ import annotations

import math
import textwrap
from typing import Callable


class Monkey:
    def __init__(
        self,
        items: list[int],
        operation: Callable[[int], int],
        test: Callable[[bool], int],
        divisor: int,
        part: int,
    ) -> None:
        self.items = items
        self.inspect_count = 0
        self.operation = operation
        self.test = test
        self.divisor = divisor
        self.part = part

    def do_turn(self, troop: list[Monkey], lcm: int) -> None:
        while self.items:
            self.inspect_count += 1
            item = self.operation(self.items.pop(0))
            if self.part == 1:
                item //= 3
            item %= lcm
            target_monkey = self.test(item % self.divisor == 0)
            troop[target_monkey].items.append(item)

    @classmethod
    def create_from_string(cls, monkey_string: str, part: int) -> Monkey:
        lines = monkey_string.lower().splitlines()
        exec_string = f"""\
            def test(cond):
                if cond:
                    return {lines[4].split()[-1]}
                else:
                    return {lines[5].split()[-1]}
            monkey = cls(
                items=[{lines[1].partition(": ")[2]}],
                operation=lambda old: {lines[2].partition("= ")[2]},
                test=test,
                divisor={lines[3].split()[-1]},
                part=part
            )"""
        local_dict = {"cls": cls, "part": part}
        exec(textwrap.dedent(exec_string), globals(), local_dict)
        return local_dict.get("monkey")  # type: ignore


def compute(s: str, part: int) -> int:
    troop = []
    for monkey_str in s.split("\n\n"):
        troop.append(Monkey.create_from_string(monkey_str, part))
    lcm = math.lcm(*set(map(lambda x: x.divisor, troop)))
    for _ in range(10_000 if part == 2 else 20):
        for monkey in troop:
            monkey.do_turn(troop, lcm)
    counts = list(sorted(map(lambda x: x.inspect_count, troop), reverse=True))
    return counts[0] * counts[1]


if __name__ == "__main__":
    with open(0) as f:
        input_str = f.read()
        print(compute(input_str, 1))
        print(compute(input_str, 2))
