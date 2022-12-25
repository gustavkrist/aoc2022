trees = [tuple(map(int, line.rstrip())) for line in open(0).read().splitlines()]
trees_t = tuple(zip(*trees))
highest = 0
height, width = len(trees), len(trees[0])
for rownum, row in enumerate(trees):
    if rownum in [0, height - 1]:
        continue
    for colnum, tree in enumerate(row):
        if colnum in [0, width - 1]:
            continue
        left = right = up = down = 0
        for left, other_tree in enumerate(row[colnum - 1::-1], start=1):
            if tree <= other_tree:
                break
        for right, other_tree in enumerate(row[colnum + 1:], start=1):
            if tree <= other_tree:
                break
        for up, other_tree in enumerate(trees_t[colnum][rownum - 1::-1], start=1):
            if tree <= other_tree:
                break
        for down, other_tree in enumerate(trees_t[colnum][rownum + 1:], start=1):
            if tree <= other_tree:
                break
        total = left * right * up * down
        highest = max(total, highest)
print(highest)
