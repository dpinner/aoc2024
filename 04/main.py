import sys
from collections import deque, defaultdict
from typing import List, Tuple


def search(grid: List[str], word: str) -> List[List[Tuple[int, int]]]:
    if len(word) == 0:
        return []
    candidates = deque()
    for i in range(len(grid)):
        j = grid[i].find(word[0])
        while j != -1:
            candidates.append([(i, j)])
            j = grid[i].find(word[0], j + 1)

    coords = []
    while candidates:
        c = candidates.popleft()
        if len(c) >= len(word):
            coords.append(c)
            continue
        dirs = (
            [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]
            if len(c) == 1
            else [(c[1][0] - c[0][0], c[1][1] - c[0][1])]
        )
        target = word[len(c)]
        for dir in dirs:
            new_x = c[-1][0] + dir[0]
            new_y = c[-1][1] + dir[1]
            if (
                new_x >= len(grid)
                or new_x < 0
                or new_y >= len(grid[c[-1][0]])
                or new_y < 0
            ):
                continue
            if grid[new_x][new_y] == target:
                candidates.append([*c, (new_x, new_y)])
    return coords


def xsearch(grid: List[str], word: str) -> int:
    center = len(word) // 2
    matches = search(grid, word)
    candidates = defaultdict(set)
    for m in matches:
        dir_x = m[1][0] - m[0][0]
        dir_y = m[1][1] - m[0][1]
        if dir_x == 0 or dir_y == 0:
            continue
        candidates[m[center]].add((dir_x, dir_y))
    return sum(1 for dirs in candidates.values() if len(dirs) >= 2)


if __name__ == "__main__":
    filename = sys.argv[1]
    grid = []
    with open(filename, "r") as f:
        grid = f.read().splitlines()

    print(len(search(grid, "XMAS")))
    print(xsearch(grid, "MAS"))
