from collections import deque
from copy import deepcopy

with open(0) as f:
    crate_lines = []
    for line in f:
        if not line.rstrip():
            break
        crate_lines.append(line.rstrip())
    crates1: list[deque[str]] = [deque() for _ in range(int(crate_lines.pop()[-1]))]
    for line in crate_lines:
        for crate, let in enumerate(range(1, len(line) + 1, 4)):
            if line[let] != " ":
                crates1[crate].appendleft(line[let])
    crates2: list[deque[str]] = deepcopy(crates1)
    for instruction in f:
        count, source, target = map(int, instruction.split()[1::2])
        tmp: deque[str] = deque()
        for _ in range(count):
            if crates1[source - 1]:
                crates1[target - 1].append(crates1[source - 1].pop())
            if crates2[source - 1]:
                tmp.appendleft(crates2[source - 1].pop())
        for letter in tmp:
            crates2[target - 1].append(letter)
    print("".join(map(lambda x: "" if not x else x[-1], crates1)))
    print("".join(map(lambda x: "" if not x else x[-1], crates2)))
