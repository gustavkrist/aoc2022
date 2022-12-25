from __future__ import annotations

import argparse
import os.path
from typing import Callable

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


class Item:
    def __init__(self, worry_level: int):
        self.worry_level = worry_level

    def __repr__(self) -> str:
        return str(self.worry_level)


class Monkey:
    def __init__(
        self,
        items: list[Item],
        operation: Callable[[int], int],
        test: Callable[[int], int],
    ) -> None:
        self.items = items
        self.inspect_count = 0
        self.operation = operation
        self.test = test

    def do_turn(self, troop: list[Monkey]) -> None:
        for item in iter(list(self.items)):
            self.inspect_count += 1
            item.worry_level = self.operation(item.worry_level) // 3
            target_monkey = self.test(item.worry_level)
            self.items.remove(item)
            troop[target_monkey].items.append(item)

    @classmethod
    def create_from_string(cls, monkey_string: str) -> Monkey:
        test_func_str = ""
        items = []
        operation_func = None
        for i, line in enumerate(monkey_string.splitlines()):
            if i == 0:
                continue
            if i == 1:
                items = list(map(lambda x: Item(int(x)), line.partition(': ')[2].split(', ')))
            if i == 2:
                _, _, func_body = line.partition(' = ')
                operation_func = eval(f'lambda old: {func_body}')
            if i == 3:
                divisible_by = int(line.split()[-1])
                test_func_str = f"""def test_worry_level(worry_level: int) -> int:\n\tif worry_level % {divisible_by} == 0:\n\t\t"""
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
        return cls(items, operation_func, test_func)


def compute(s: str) -> int:
    troop = []
    for monkey_str in s.split('\n\n'):
        troop.append(Monkey.create_from_string(monkey_str))
    for _ in range(20):
        for monkey in troop:
            monkey.do_turn(troop)
    counts = list(sorted(map(lambda x: x.inspect_count, troop), reverse=True))
    return counts[0] * counts[1]


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
