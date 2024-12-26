import sys
from typing import List, Tuple


def count_pairs(locks: List[Tuple[int]], keys: List[Tuple[int]]) -> int:
    valid_pairs = 0
    for lock in locks:
        for key in keys:
            if any(a + b > 5 for a, b in zip(lock, key)):
                continue
            valid_pairs += 1
    return valid_pairs


if __name__ == "__main__":
    filename = sys.argv[1]
    locks = []
    keys = []
    grid_height = 7
    with open(filename, "r") as f:
        x = f.read().split("\n\n")
        for grid in x:
            arr = locks if grid[0] == "#" else keys
            heights = [None] * 5
            for i, line in enumerate(grid.split("\n")):
                for k, c in enumerate(line.rstrip()):
                    if grid[0] == "#" and c == "." and heights[k] is None:
                        heights[k] = i - 1
                    elif grid[0] == "." and c == "#" and heights[k] is None:
                        heights[k] = grid_height - i - 1
            arr.append(tuple(heights))

    print(count_pairs(locks, keys))
