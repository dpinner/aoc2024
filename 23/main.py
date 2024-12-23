import sys
from math import comb
from collections import defaultdict
from typing import Dict, Set, List


def BronKerbosch(
    clique: Set[str],
    candidates: Set[str],
    exclusions: Set[str],
    edges: Dict[str, Set[str]],
    cliques: List[str],
):
    if len(candidates) == 0 and len(exclusions) == 0:
        cliques.append(",".join(sorted([n for n in clique])))
        return

    pivot = max((n for n in candidates.union(exclusions)), key=lambda n: len(edges[n]))
    for n in candidates - edges[pivot]:
        BronKerbosch(
            clique.union(set([n])),
            candidates.intersection(edges[n]),
            exclusions.intersection(edges[n]),
            edges,
            cliques,
        )
        candidates.remove(n)
        exclusions.add(n)


if __name__ == "__main__":
    filename = sys.argv[1]
    edges = defaultdict(set)
    triples = set()
    with open(filename, "r") as f:
        for line in f:
            a, b = line.rstrip().split("-")
            for c in edges[a]:
                if b in edges[c]:
                    triples.add("-".join(sorted([a, b, c])))
            edges[a].add(b)
            edges[b].add(a)

    cliques = []
    BronKerbosch(set(), set(edges.keys()), set(), edges, cliques)

    print(sum(1 for t in triples if any(c.startswith("t") for c in t.split("-"))))
    print(max(cliques, key=lambda c: len(c.split(","))))
