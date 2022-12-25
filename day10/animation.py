import os
import time


UP = "\x1B[6A"
CLR = "\x1B[0K"


def draw_pixel(image: list[list[str]], x: int, cycle: int) -> None:
    pixel = "#" if cycle % 40 in (x - 1, x, x + 1) else "."
    image[cycle // 40][cycle % 40] = pixel
    print(UP + f"{CLR}\n".join("".join(line) for line in image), end=f'{CLR}\n')
    time.sleep(0.05)


with open(0) as f:
    print("\n\n\n\n\n")
    cycle = 0
    x = 1
    image = [[" "] * 40 for _ in range(6)]
    for instruction in f.read().splitlines():
        draw_pixel(image, x, cycle)
        if len(instruction.split()) > 1:
            amount = int(instruction.split()[1])
            cycle += 1
            draw_pixel(image, x, cycle)
            x += amount
        cycle += 1
    time.sleep(2)
