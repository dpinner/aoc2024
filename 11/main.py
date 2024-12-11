import sys
from math import log10
from typing import Dict, Tuple


def blink(val: int, times: int, memo: Dict[Tuple[int, int], int]) -> int:
    if (val, times) in memo:
        return memo[(val, times)]

    if times == 0:
        return 1

    if val == 0:
        memo[(val, times)] = blink(1, times - 1, memo)
        return memo[(val, times)]

    digits = int(1 + log10(val))
    if digits % 2 == 0:
        pow = 10 ** (digits // 2)
        memo[(val, times)] = blink(val // pow, times - 1, memo) + blink(
            val % pow, times - 1, memo
        )
        return memo[(val, times)]

    memo[(val, times)] = blink(val * 2024, times - 1, memo)
    return memo[(val, times)]


if __name__ == "__main__":
    filename = sys.argv[1]
    blinks = int(sys.argv[2])
    memo = {}
    with open(filename, "r") as f:
        vals = list(map(int, f.read().split()))

    print(sum(blink(v, blinks, memo) for v in vals))
