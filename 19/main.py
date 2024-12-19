import sys
from functools import lru_cache
from typing import List


@lru_cache()
def combinations(towel: str) -> bool:
    n = 0
    if len(towel) == 0:
        return 1
    for pat in avail:
        if towel == pat:
            n += 1
        elif towel[: len(pat)] == pat:
            n += combinations(towel[len(pat) :])

    return n


if __name__ == "__main__":
    filename = sys.argv[1]
    global avail
    desired: List[str]
    with open(filename, "r") as f:
        avail = set(x.strip() for x in next(f).strip().split(","))
        next(f)
        desired = f.read().splitlines()

    print(sum(combinations(p) > 0 for p in desired))
    print(sum(combinations(p) for p in desired))
