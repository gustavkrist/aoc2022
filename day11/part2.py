from __future__ import annotations

import argparse
import os.path
import math
from typing import Callable

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


class Monkey:
    def __init__(
        self,
        items: list[int],
        operation: Callable[[int], int],
        test: Callable[[int], int],
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
            item = self.items.pop(0)
            item = self.operation(item)
            if self.part == 1:
                item //= 3
            item %= lcm
            target_monkey = self.test(item % self.divisor == 0)
            troop[target_monkey].items.append(item)

    @classmethod
    def create_from_string(cls, monkey_string: str, part: int) -> Monkey:
        test_func_str = ""
        items = []
        operation_func = None
        divisor = None
        for i, line in enumerate(monkey_string.splitlines()):
            if i == 0:
                continue
            if i == 1:
                items = list(map(lambda x: int(x), line.partition(': ')[2].split(', ')))
            if i == 2:
                _, _, func_body = line.partition(' = ')
                operation_func = eval(f'lambda old: {func_body}')
            if i == 3:
                divisor = int(line.split()[-1])
                test_func_str = """def test_worry_level(cond: bool) -> int:\n\tif cond:\n\t\t"""
            if i == 4:
                target_monkey = int(line.split()[-1])
                test_func_str += f"return {target_monkey}\n\telse:\n\t\t"
            if i == 5:
                target_monkey = int(line.split()[-1])
                test_func_str += f"return {target_monkey}"
        local_dict: dict[str, Callable[[int], int]] = {}
        exec(test_func_str, globals(), local_dict)
        test_func = local_dict.get('test_worry_level')
        assert test_func is not None
        assert operation_func is not None
        assert divisor is not None
        return cls(items, operation_func, test_func, divisor, part)


def compute(s: str) -> int:
    troop = []
    for monkey_str in s.split('\n\n'):
        troop.append(Monkey.create_from_string(monkey_str, 2))
    lcm = math.lcm(*set(map(lambda x: x.divisor, troop)))
    for _ in range(10000):
        for monkey in troop:
            monkey.do_turn(troop, lcm)
    counts = list(sorted(map(lambda x: x.inspect_count, troop), reverse=True))
    return counts[0] * counts[1]


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
