import sys
from collections import deque
from functools import cache
from typing import Dict, List, Literal

numpad = {
    "A": 2 + 3j,
    "0": 1 + 3j,
    "#": 3j,
    "1": 2j,
    "2": 1 + 2j,
    "3": 2 + 2j,
    "4": 1j,
    "5": 1 + 1j,
    "6": 2 + 1j,
    "7": 0,
    "8": 1,
    "9": 2,
}
numgrid = {v: k for k, v in numpad.items()}
dirpad = {"A": 2, "^": 1, "#": 0, "<": 1j, "v": 1 + 1j, ">": 2 + 1j}
dirgrid = {v: k for k, v in dirpad.items()}

dir_map = {1: ">", -1: "<", 1j: "v", -1j: "^"}

val_map = {"<": -1, "^": 0, "v": 0, ">": 1}


@cache
def search(pos: complex, target: str, type: Literal["n", "d"]) -> List[str]:
    q = deque([(0, pos, "")])
    dirs = [1, -1, 1j, -1j]
    seen = {}
    paths = []
    grid = numgrid if type == "n" else dirgrid
    while q:
        steps, loc, path = q.popleft()
        seen[loc] = steps
        if grid[loc] == target:
            paths.append(path)
            continue
        q += [
            (steps + 1, loc + d, path + dir_map[d])
            for d in dirs
            if seen.get(loc + d, float("inf")) >= steps + 1
            and loc + d in grid
            and grid[loc + d] != "#"
        ]
    return min(
        paths,
        key=lambda p: (
            0 if len(p) <= 2 else sum(a != b for a, b in zip(p, p[1:])),
            sum(val_map[b] < val_map[a] for a, b in zip(p, p[1:])),
        ),
    )


def program(code: str, type: Literal["n", "d"] = "d"):
    pad = numpad if type == "n" else dirpad
    pos = pad["A"]
    for c in code:
        yield search(pos, c, type) + "A"
        pos = pad[c]

    return


@cache
def count(code: str, n: int):
    if n == 0:
        return len(code)

    return sum(count(chunk, n - 1) for chunk in program(code))


if __name__ == "__main__":
    filename = sys.argv[1]
    codes = []
    with open(filename, "r") as f:
        for line in f:
            codes.append(line.rstrip())

    part1 = 0
    part2 = 0
    for code in codes:
        r1 = "".join(program(code, "n"))
        for i in range(25):
            count(r1, i)

        part1 += int(code[:-1]) * count(r1, 2)
        part2 += int(code[:-1]) * count(r1, 25)

    print(part1, part2)
