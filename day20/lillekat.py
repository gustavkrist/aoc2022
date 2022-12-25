from copy import copy
from dataclasses import dataclass


@dataclass
class Number:
    val: int

    def __eq__(self, other: object) -> bool:
        return self is other


def part1(s: str) -> int:
    numbers = list(map(lambda x: Number(int(x)), s.splitlines()))
    process_order = copy(numbers)
    for number in process_order:
        if number.val == 0:
            continue
        new_idx = (numbers.index(number) + number.val) % (len(numbers) - 1)
        numbers.remove(number)
        numbers.insert(new_idx, number)
    zero_idx = numbers.index(next(filter(lambda x: x.val == 0, numbers)))
    return sum(numbers[(zero_idx + i * 1000) % len(numbers)].val for i in range(1, 4))


def part2(s: str) -> int:
    numbers = list(map(lambda x: Number(int(x) * 811589153), s.splitlines()))
    process_order = copy(numbers)
    for _ in range(10):
        for number in process_order:
            if number.val == 0:
                continue
            new_idx = (numbers.index(number) + number.val) % (len(numbers) - 1)
            numbers.remove(number)
            numbers.insert(new_idx, number)
    zero_idx = numbers.index(next(filter(lambda x: x.val == 0, numbers)))
    return sum(numbers[(zero_idx + i * 1000) % len(numbers)].val for i in range(1, 4))


with open(0) as f:
    s = f.read().rstrip()
    print(part1(s))
    print(part2(s))
