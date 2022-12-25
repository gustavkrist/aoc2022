def draw_pixel(image: list[list[str]], x: int, cycle: int) -> None:
    pixel = '█' if cycle % 40 in (x - 1, x, x + 1) else '.'
    image[cycle // 40][cycle % 40] = pixel


with open(0) as f:
    cycle = 1
    x = 1
    part1 = 0
    image = [[' '] * 40 for _ in range(6)]
    for instruction in f.read().splitlines():
        draw_pixel(image, x, cycle - 1)
        if (cycle - 20) % 40 == 0:
            part1 += cycle * x
        if len(instruction.split()) > 1:
            amount = int(instruction.split()[1])
            cycle += 1
            draw_pixel(image, x, cycle - 1)
            if (cycle - 20) % 40 == 0:
                part1 += cycle * x
            x += amount
        cycle += 1
    print(part1)
    print('\n'.join(''.join(line) for line in image))
