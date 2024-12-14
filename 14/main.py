import sys
import re
from collections import deque


def safety(pos, vel, moves, width, height):

    counts = [0] * 4
    new_pos = move(pos, vel, moves, width, height)
    for r in new_pos:
        if r[0] < (width - 1) / 2 and r[1] < (height - 1) / 2:
            counts[0] += 1
        elif r[0] > (width - 1) / 2 and r[1] < (height - 1) / 2:
            counts[1] += 1
        elif r[0] > (width - 1) / 2 and r[1] > (height - 1) / 2:
            counts[2] += 1
        elif r[0] < (width - 1) / 2 and r[1] > (height - 1) / 2:
            counts[3] += 1

    res = 1
    for c in counts:
        res *= c
    return res


def move(pos, vel, moves, width, height):
    return [
        ((p[0] + moves * v[0]) % width, (p[1] + moves * v[1]) % height)
        for p, v in zip(pos, vel)
    ]


# return the number of moves that results in the fewest disconnected regions
def easter_egg(pos, vel, max_moves, width, height):
    min_disconnected = len(pos)
    idx = 0
    dirs = [(0, 1), (-1, 0), (0, -1), (1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for i in range(max_moves):
        seen = set()
        disconnected = 0
        new_pos = set(move(pos, vel, i, width, height))
        for p in new_pos:
            if p in seen:
                continue
            q = deque([p])
            while q:
                x = q.popleft()
                if x in seen:
                    continue
                seen.add(x)
                ns = [(x[0] + d[0], x[1] + d[1]) for d in dirs]
                if not any(n in new_pos for n in ns):
                    disconnected += 1
                q += [n for n in ns if n in new_pos]
        if disconnected < min_disconnected:
            min_disconnected = disconnected
            idx = i

    return idx


if __name__ == "__main__":

    filename = sys.argv[1]
    pos = []
    vel = []
    with open(filename, "r") as f:
        for line in f:
            px, py, vx, vy = re.findall(r"-*\d+", line)
            pos.append((int(px), int(py)))
            vel.append((int(vx), int(vy)))

    # print(safety(pos, vel, 100, 11, 7))
    print(safety(pos, vel, 100, 101, 103))
    idx = easter_egg(pos, vel, 10000, 101, 103)

    print(idx)
    for y in range(103):
        print(
            "".join(
                (
                    " " if (x, y) not in set(move(pos, vel, idx, 101, 103)) else "*"
                    for x in range(101)
                )
            )
        )
