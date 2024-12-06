import sys
from typing import Dict, Set, Tuple


def path(
    start: complex, dir: complex, grid: Dict[complex, str]
) -> Tuple[Set[complex], bool]:
    visited = set()
    loop = False
    loc = start
    while loc in grid and not loop:
        if (loc, dir) in visited:
            loop = True
        visited.add((loc, dir))
        while grid.get(loc + dir) == "#":
            dir *= 1j
        loc += dir

    return set(loc for loc, _ in visited), loop


if __name__ == "__main__":
    filename = sys.argv[1]
    grid = {}
    start = 0
    dir = 0
    with open(filename, "r") as f:
        i = 0
        for line in f:
            for k, c in enumerate(line.rstrip()):
                loc = k + 1j * i
                grid[loc] = c
                if c == "^":
                    start = loc
                    dir = -1j
                elif c == ">":
                    start = loc
                    dir = 1
                elif c == "<":
                    start = loc
                    dir = -1
                elif c == "v":
                    start = loc
                    dir = 1j
            i += 1

    visited = path(start, dir, grid)[0]

    print(len(visited))

    obs = 0
    for loc in visited:
        if loc == start or grid[loc] == "#":
            continue
        grid[loc] = "#"
        if path(start, dir, grid)[1]:
            obs += 1
        grid[loc] = "."

    print(obs)
