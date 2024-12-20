import sys
from collections import deque
from typing import Dict


def count_steps(
    start: complex, grid: Dict[complex, str], step_counts: Dict[complex, int]
):
    q = deque([(0, start)])
    dirs = [-1, 1, -1j, 1j]
    while q:
        steps, pos = q.popleft()
        step_counts[pos] = steps
        if grid[pos] == "E":
            return
        q += [
            (steps + 1, pos + d)
            for d in dirs
            if pos + d not in step_counts and pos + d in grid and grid[pos + d] != "#"
        ]


def count_cheats(step_counts: Dict[complex, int], threshold: int, duration: int) -> int:
    cheats = 0
    for loc_1, steps_1 in step_counts.items():
        for x in range(-duration, duration + 1):
            for y in range(-duration + abs(x), duration + 1 - abs(x)):
                loc_2 = loc_1 + x + y * 1j

                steps_2 = step_counts.get(loc_2, 0)

                if steps_2 - steps_1 - abs(x) - abs(y) >= threshold:
                    cheats += 1

    return cheats


if __name__ == "__main__":
    filename = sys.argv[1]
    grid: Dict[complex, str] = {}
    dir = 0
    with open(filename, "r") as f:
        grid = {
            k + i * 1j: c
            for i, line in enumerate(f)
            for k, c in enumerate(line.rstrip())
        }

    for loc in grid:
        if grid[loc] == "S":
            start = loc
            break

    step_counts = {}
    count_steps(start, grid, step_counts)

    print(count_cheats(step_counts, 100, 2))
    print(count_cheats(step_counts, 100, 20))
