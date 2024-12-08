import sys
from collections import defaultdict
from typing import Dict, List, Set, Tuple


def antinodes(n: int, m: int, antennas: Dict[str, List[complex]]) -> Tuple[int, int]:
    x: Set[complex] = set()
    y: Set[complex] = set()

    for locs in antennas.values():
        for i, loc1 in enumerate(locs):
            for loc2 in locs[i + 1 :]:

                antinode = loc2
                c = 0

                while 0 <= antinode.real < m and 0 <= antinode.imag < n:
                    if c == 1:
                        x.add(antinode)
                    y.add(antinode)
                    c += 1
                    antinode += loc2 - loc1

                antinode = loc1
                c = 0

                while 0 <= antinode.real < m and 0 <= antinode.imag < n:
                    if c == 1:
                        x.add(antinode)
                    y.add(antinode)
                    c += 1
                    antinode += loc1 - loc2

    return len(x), len(y)


if __name__ == "__main__":
    filename = sys.argv[1]
    antennas: Dict[str, List[complex]] = defaultdict(list)
    with open(filename, "r") as f:
        i = 0
        for line in f:
            for k, c in enumerate(line.rstrip()):
                if c == ".":
                    continue
                antennas[c].append(k + 1j * i)
            i += 1

    print(antinodes(i, k + 1, antennas))
