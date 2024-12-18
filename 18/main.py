import sys
from collections import deque
from typing import Tuple, Set, Optional


def shortest_path(
    target: Tuple[int, int], blocks: Set[Tuple[int, int]]
) -> Optional[int]:
    xt, yt = target
    q = deque([(0, 0, 0)])
    seen = {}
    dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    while q:
        cost, x, y = q.popleft()
        if (x, y) == target:
            return cost
        for dx, dy in dirs:
            xp = x + dx
            yp = y + dy
            if (
                xp > xt
                or xp < 0
                or yp > yt
                or yp < 0
                or (xp, yp) in blocks
                or (xp, yp) in seen
            ):
                continue
            seen[(xp, yp)] = cost + 1
            q.append((cost + 1, xp, yp))

    return None


if __name__ == "__main__":
    filename = sys.argv[1]
    cutoff = int(sys.argv[2])
    blocks = []
    with open(filename, "r") as f:
        for line in f:
            x, y = line.rstrip().split(",")
            blocks.append((int(x), int(y)))

    # print(shortest_path((6, 6), set(blocks[:cutoff])))
    print(shortest_path((70, 70), set(blocks[:cutoff])))

    l, r = cutoff, len(blocks) - 1
    while l < r:
        mid = l + (r - l) // 2
        if shortest_path((70, 70), set(blocks[:mid])):
            l = mid + 1
        else:
            r = mid - 1

    print(blocks[l - 1])
