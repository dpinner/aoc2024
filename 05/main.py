import sys
from collections import defaultdict
from functools import cmp_to_key
from typing import Dict, List, Set


def is_valid(update: List[str], edges: Dict[str, Set[str]]) -> bool:
    for i, val in enumerate(update):
        if len(set(update[:i]) & edges[val]) > 0:
            return False
    return True


if __name__ == "__main__":
    filename = sys.argv[1]
    edges = defaultdict(set)
    updates = []
    with open(filename, "r") as f:
        for line in f:
            if not line.rstrip():
                continue
            edge = line.rstrip().split("|")
            if len(edge) > 1:
                edges[edge[0]].add(edge[1])
            else:
                updates.append(line.rstrip().split(","))

    tot = sum(int(x[len(x) // 2]) for x in updates if is_valid(x, edges))
    cmp = lambda x, y: -1 if y in edges[x] else 1 if x in edges[y] else 0
    sorted_tot = sum(
        int(sorted(x, key=cmp_to_key(cmp))[len(x) // 2])
        for x in updates
        if not is_valid(x, edges)
    )
    print(tot, sorted_tot)
