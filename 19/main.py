import sys
from typing import Dict, List, Set


def dp(towel: str, longest: int, avail: Set[str], memo: Dict[str, int]) -> int:
    if towel in memo:
        return
    memo[towel] = 1 if towel in avail else 0
    n = 0
    for j in range(1, longest + 1):
        if towel[:j] in avail:
            n += memo[towel[j:]]

    memo[towel] += n


if __name__ == "__main__":
    filename = sys.argv[1]
    desired: List[str]
    with open(filename, "r") as f:
        avail = set(x.strip() for x in next(f).strip().split(","))
        next(f)
        desired = f.read().splitlines()

    memo = {"": 0}
    longest = max(len(p) for p in avail)
    n = 0
    count = 0
    for p in desired:
        i = len(p) - 1
        while i >= 0:
            substr = p[i:]
            dp(substr, longest, avail, memo)
            i -= 1
        n += memo[p]
        count += 1 if memo[p] > 0 else 0

    print(count, n)
