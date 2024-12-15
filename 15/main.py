import sys
from collections import deque
from typing import Dict


def score(grid: Dict[complex, str]) -> int:
    tot = 0
    for loc in grid:
        if grid[loc] != "O" and grid[loc] != "[":
            continue
        tot += 100 * int(loc.imag) + int(loc.real)
    return tot


move_map: Dict[str, complex] = {"<": -1, "v": 1j, "^": -1j, ">": 1}


def is_block(grid: Dict[complex, str], loc: complex) -> bool:
    return loc in grid and grid[loc] in "O[]"


def wide_slide(grid: Dict[complex, str], pos: complex, d: str) -> bool:
    blocks = set()
    q = deque([pos])
    while q:
        b = q.popleft()
        next_loc = b + move_map[d]
        if is_block(grid, next_loc):
            blocks.add(next_loc)
            adj = next_loc + 1 if grid[next_loc] == "[" else next_loc - 1
            blocks.add(adj)
            q += [next_loc, adj]

    if any(b + move_map[d] in grid and grid[b + move_map[d]] == "#" for b in blocks):
        return False

    grid_update = {b: "." for b in blocks}
    for b in blocks:
        grid_update[b + move_map[d]] = grid[b]

    grid.update(grid_update)

    return True


def slide(grid: Dict[complex, str], pos: complex, d: str) -> bool:
    if grid[pos + move_map[d]] in "[]" and d in "v^":
        return wide_slide(grid, pos, d)
    n = 1
    while is_block(grid, pos + n * move_map[d]):
        n += 1

    if grid[pos + (n) * move_map[d]] == "#":
        return False

    if grid[pos + move_map[d]] == "O":
        grid[pos + n * move_map[d]] = "O"
        grid[pos + move_map[d]] = "."
    else:
        for i in range(n, 0, -1):
            grid[pos + i * move_map[d]] = grid[pos + (i - 1) * move_map[d]]

    return True


def move(grid: Dict[complex, str], pos: complex, d: str) -> complex:
    if pos + move_map[d] not in grid or grid[pos + move_map[d]] == "#":
        return pos

    if not is_block(grid, pos + move_map[d]):
        return pos + move_map[d]

    success = slide(grid, pos, d)
    return pos if not success else pos + move_map[d]


def vis(grid: Dict[complex, str]):
    max_x = max(int(x.real) for x in grid)
    max_y = max(int(x.imag) for x in grid)
    for k in range(max_y + 1):
        print("".join(grid[i + k * 1j] for i in range(max_x + 1)))


if __name__ == "__main__":
    filename = sys.argv[1]
    grid: Dict[complex, int] = {}
    dgrid: Dict[complex, int] = {}
    move_list = []
    with open(filename, "r") as f:
        for i, line in enumerate(f):
            if line[0] == "#":
                for k, c in enumerate(line.rstrip()):
                    grid[k + i * 1j] = c
                    if c == "." or c == "#":
                        dgrid[2 * k + i * 1j] = c
                        dgrid[2 * k + 1 + i * 1j] = c
                    if c == "@":
                        grid[k + i * 1j] = "."
                        dgrid[2 * k + i * 1j] = "."
                        dgrid[2 * k + 1 + i * 1j] = "."
                        start = k + i * 1j
                    if c == "O":
                        dgrid[2 * k + i * 1j] = "["
                        dgrid[2 * k + 1 + i * 1j] = "]"
            else:
                move_list.append(line.rstrip())

    moves = "".join(move_list)
    pos = start
    dpos = start + int(start.real)
    for d in moves:
        pos = move(grid, pos, d)
        dpos = move(dgrid, dpos, d)

    print(score(grid))
    print(score(dgrid))
