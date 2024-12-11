import sys
from math import ceil, log10
from typing import Dict, Tuple


def blink(val: int, times: int, memo: Dict[Tuple[int, int], int]) -> int:
    if (val, times) in memo:
        return memo[(val, times)]

    if times == 0:
        return 1

    if val == 0:
        count = blink(1, times - 1, memo)
        memo[(val, times)] = count
        return count

    log_val = log10(val)
    digits = ceil(log_val)
    if digits == log_val:
        digits += 1
    if digits % 2 == 0:
        pow = 10 ** (digits // 2)
        left_val, right_val = val // pow, val % pow
        count = blink(left_val, times - 1, memo) + blink(right_val, times - 1, memo)
        memo[(val, times)] = count
        return count

    count = blink(val * 2024, times - 1, memo)
    memo[(val, times)] = count
    return count


if __name__ == "__main__":
    filename = sys.argv[1]
    blinks = int(sys.argv[2])
    memo = {}
    with open(filename, "r") as f:
        vals = list(map(int, f.read().split()))

    print(sum(blink(v, blinks, memo) for v in vals))
