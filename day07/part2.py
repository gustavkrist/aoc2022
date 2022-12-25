from __future__ import annotations

import argparse
import os.path
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")
SAMPLES = os.path.join(os.path.dirname(__file__), "samples")


def compute(s: str) -> int:
    lines = list(reversed(s.rstrip().splitlines()))
    dirs: dict[str, int] = defaultdict(int)

    def find_size(path: str) -> None:
        while lines:
            line = lines.pop()
            if line.startswith("$"):
                if "$ cd" in line:
                    dir = line.split("cd ")[-1]
                    if dir == '..':
                        return
                    else:
                        if path == '/':
                            find_size(path + f'{dir}')
                        else:
                            find_size(path + f'/{dir}')
                else:
                    continue
            else:
                typeof, name = line.split(' ')
                if typeof == 'dir':
                    pass
                else:
                    dir = path
                    while os.path.dirname(dir) != '/':
                        dirs[dir] += int(typeof)
                        dir = os.path.dirname(dir)
                    dirs['/'] += int(typeof)

    dir = lines.pop().split("cd ")[-1]
    find_size(dir)
    available = 70_000_000 - dirs['/']
    necessary = 30_000_000 - available
    return min(v for v in dirs.values() if v >= necessary)


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
