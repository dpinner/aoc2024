import sys
from collections import deque
from typing import Dict, Set, Tuple


def search(start: complex, grid: Dict[complex, str]) -> Tuple[int, int]:
    q = deque([(0, (start,))])
    best_path_locs = set()
    seen = {}
    min_cost = float("inf")
    while q:
        cost, path = q.popleft()
        if cost > min_cost:
            continue
        pos = path[-1]
        o = path[-1] - path[-2] if len(path) >= 2 else 1
        seen[pos] = cost
        if grid[pos] == "E":
            best_path_locs = (
                {l for l in path}
                if cost < min_cost
                else best_path_locs | {l for l in path}
            )
            min_cost = cost
            continue
        for d in [o, o * 1j, -o * 1j]:
            if pos + d not in grid or grid[pos + d] == "#":
                continue
            delta_cost = 1001 if d != o else 1
            if pos + d in seen and seen[pos + d] < cost + delta_cost:
                continue
            q.append((cost + delta_cost, (*path, pos + d)))

    return min_cost, len(best_path_locs)


def vis(grid: Dict[complex, str]):
    max_x = max(int(x.real) for x in grid)
    max_y = max(int(x.imag) for x in grid)
    for k in range(max_y + 1):
        print("".join(grid[i + k * 1j] for i in range(max_x + 1)))


if __name__ == "__main__":
    filename = sys.argv[1]
    grid: Dict[complex, int] = {}
    with open(filename, "r") as f:
        grid = {
            k + i * 1j: c
            for i, line in enumerate(f)
            for k, c in enumerate(line.rstrip())
        }

    start = 0
    for loc in grid:
        if grid[loc] == "S":
            start = loc
            break

    print(search(start, grid))
