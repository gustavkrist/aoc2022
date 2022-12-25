def part1(input: str) -> int:
    return sum(
        1 if len(set1 & set2) in [len(set1), len(set2)] else 0
        for line in input.splitlines()
        for set1, set2 in map(
            lambda x: (set(range(x[0], x[1] + 1)), set(range(x[2], x[3] + 1))),
            (list(map(int, line.replace("-", ",").split(","))),),
        )
    )


def part2(input: str) -> int:
    return sum(
        1 if len(set1 & set2) > 0 else 0
        for line in input.splitlines()
        for set1, set2 in map(
            lambda x: (set(range(x[0], x[1] + 1)), set(range(x[2], x[3] + 1))),
            (list(map(int, line.replace("-", ",").split(","))),),
        )
    )


def solve(input: str) -> tuple[int, int]:
    return tuple(map(sum, zip(*[
        (int(len(set1 & set2) in [len(set1), len(set2)]), int(len(set1 & set2) > 0))
        for line in input.splitlines()
        for set1, set2 in map(
            lambda x: (set(range(x[0], x[1] + 1)), set(range(x[2], x[3] + 1))),
            (list(map(int, line.replace("-", ",").split(","))),),
        )
    ])))
