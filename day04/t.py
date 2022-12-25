# with open(0) as f:
#     part1 = part2 = 0
#     for line in f:
#         nums = list(map(int, line.replace('-', ',').split(',')))
#         set1, set2 = set(range(nums[0], nums[1] + 1)), set(range(nums[2], nums[3] + 1))
#         part1 += int(len(set1 & set2) in [len(set1), len(set2)])
#         part2 += int(len(set1 & set2) > 0)
#     print(part1)
#     print(part2)


print(tuple(map(sum, zip(*[
        (int(len(set1 & set2) in [len(set1), len(set2)]), int(len(set1 & set2) > 0))
        for line in open(0)
        for set1, set2 in map(
            lambda x: (set(range(x[0], x[1] + 1)), set(range(x[2], x[3] + 1))),
            (list(map(int, line.replace("-", ",").split(","))),),
        )
    ])))
)


with open(0) as f:
    total = 0
    for line in f:
        elf1, elf2 = map(lambda x: x.split('-'), line.split(','))
        set1, set2 = map(lambda x: set(range(int(x[0]), int(x[1]) + 1)), [elf1, elf2])
        if len(set1 & set2) in [len(set1), len(set2)]:
            total += 1
    print(total)
