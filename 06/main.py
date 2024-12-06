import sys
from typing import Dict, Tuple


def count(loc: complex, dir: complex, grid: Dict[complex, str]) -> Tuple[int, bool]:
    visited = set()
    loop = False
    while loc in grid and not loop:
        if (loc, dir) in visited:
            loop = True
        visited.add((loc, dir))
        while grid.get(loc + dir) == "#":
            dir *= 1j
        loc += dir

    return len(set(loc for loc, _ in visited)), loop


if __name__ == "__main__":
    filename = sys.argv[1]
    grid = {}
    start = 0
    dir = 0
    with open(filename, "r") as f:
        i = 0
        for line in f:
            for k, c in enumerate(line.rstrip()):
                grid[k + 1j * i] = c
                if c == "^":
                    start = k + 1j * i
                    dir = -1j
                elif c == ">":
                    start = k + 1j * i
                    dir = 1
                elif c == "<":
                    start = k + 1j * i
                    dir = -1
                elif c == "v":
                    start = k + 1j * i
                    dir = 1j
            i += 1

    print(count(start, dir, grid)[0])

    obs = 0
    for loc in grid:
        if loc == start or grid[loc] == "#":
            continue
        grid[loc] = "#"
        if count(start, dir, grid)[1]:
            obs += 1
        grid[loc] = "."

    print(obs)
