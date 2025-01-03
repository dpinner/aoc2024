import sys
from collections import deque
from typing import Dict, Set, Tuple


def rating(trailhead: complex, grid: Dict[complex, int]) -> Tuple[int, int]:
    dirs = set([1j, 1, -1, -1j])
    q = deque([(0, (trailhead,))])
    peaks = set()
    paths = set()
    while q:
        val, path = q.popleft()
        loc = path[-1]
        if val == 9:
            peaks.add(loc)
            paths.add(path)
            continue
        q += [
            (val + 1, (*path, loc + dir))
            for dir in dirs
            if loc + dir in grid and grid[loc + dir] == val + 1
        ]

    return len(peaks), len(paths)


if __name__ == "__main__":
    filename = sys.argv[1]
    grid: Dict[complex, int] = {}
    trailheads: Set[complex] = set()
    dir = 0
    with open(filename, "r") as f:
        grid = {
            k + i * 1j: int(c)
            for i, line in enumerate(f)
            for k, c in enumerate(line.rstrip())
        }
    trailheads = {loc for loc in grid if grid[loc] == 0}
    print([sum(x) for x in zip(*(rating(t, grid) for t in trailheads))])
