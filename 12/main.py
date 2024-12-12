import sys
from collections import deque
from typing import Dict, Set, Tuple


def count_sides(region: Set[complex], rotate: bool) -> int:
    sides = 0
    r = {(z * -1j).conjugate() for z in region} if rotate else region
    prev_bdys = set()
    bdys = set()
    z_prev = -1 - 1j
    for z in sorted(r, key=lambda z: (z.imag, z.real)):
        if z.imag != z_prev.imag:
            if z_prev.real != -1:
                bdys.add(z_prev.real + 0.1)
            sides += len(bdys - prev_bdys)
            z_prev = -1 + z.imag * 1j
            prev_bdys = bdys
            bdys = set()

        if z_prev.real == -1:
            bdys.add(z.real - 0.1)
        elif z.real > z_prev.real + 1:
            bdys |= {z.real - 0.1, z_prev.real + 0.1}

        z_prev = z

    if z_prev.real != -1:
        bdys.add(z_prev.real + 0.1)
    sides += len(bdys - prev_bdys)
    return sides


def cost(grid: Dict[complex, str]) -> Tuple[int, int]:
    seen: Set[complex] = set()
    tot = 0
    disc_tot = 0
    dirs = [1, -1, 1j, -1j]
    for loc in grid:
        if loc in seen:
            continue

        q = deque([loc])
        region = set()
        perimeter = 0
        while q:
            l = q.popleft()
            if l in seen:
                continue
            perimeter += 4
            region.add(l)
            seen.add(l)
            for dir in dirs:
                if l + dir in grid and grid[l + dir] == grid[l]:
                    perimeter -= 1
                    q.append((l + dir))

        tot += len(region) * perimeter
        sides = count_sides(region, True) + count_sides(region, False)
        disc_tot += len(region) * sides
    return tot, disc_tot


if __name__ == "__main__":
    filename = sys.argv[1]
    grid: Dict[complex, int] = {}
    dir = 0
    with open(filename, "r") as f:
        grid = {
            k + i * 1j: c
            for i, line in enumerate(f)
            for k, c in enumerate(line.rstrip())
        }

    print(cost(grid))
