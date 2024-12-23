import sys
from collections import defaultdict
from typing import Dict, Tuple


def step(secret: int, n: int, bananas: Dict[Tuple[int, int, int, int], int]):
    changes = []

    v = secret
    seen = set()
    for _ in range(n, 0, -1):
        t1 = (v ^ (v << 6)) % (2**24)
        t2 = (t1 ^ (t1 >> 5)) % (2**24)
        t3 = (t2 ^ (t2 << 11)) % (2**24)
        if len(changes) < 4:
            changes.append((t3 % 10) - (v % 10))
        else:
            changes[:3] = changes[1:]
            changes[3] = (t3 % 10) - (v % 10)
            k = tuple(changes)
            if k not in seen:
                bananas[k] += t3 % 10
            seen.add(k)
        v = t3

    return v


if __name__ == "__main__":
    filename = sys.argv[1]
    secrets = []
    with open(filename, "r") as f:
        for line in f:
            secrets.append(int(line.rstrip()))

    part1 = 0
    bananas = defaultdict(int)
    for secret in secrets:
        part1 += step(secret, 2000, bananas)

    print(part1, max(bananas.values()))
