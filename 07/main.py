import sys
from math import log
from typing import List, Set


def is_valid(target: int, vals: List[int], operators: Set[str]) -> bool:
    if len(vals) == 0:
        return target == 0

    if len(vals) == 1:
        return target == vals[0]

    if (
        "+" in operators
        and target >= vals[-1]
        and is_valid(target - vals[-1], vals[:-1], operators)
    ):
        return True

    if (
        "*" in operators
        and target % vals[-1] == 0
        and is_valid(target // vals[-1], vals[:-1], operators)
    ):
        return True

    if "||" in operators:
        digits = int(1 + log(vals[-1], 10))
        if (
            target > vals[-1]
            and int(str(target)[-digits:]) == vals[-1]
            and is_valid(int(str(target)[:-digits]), vals[:-1], operators)
        ):
            return True

    return False


if __name__ == "__main__":
    filename = sys.argv[1]
    calibs = []
    with open(filename, "r") as f:
        for l in f.read().splitlines():
            target, vals = l.split(":")
            vals_list = list(map(int, vals.split()))

            calibs.append((int(target), vals_list))

    print(sum(x[0] for x in calibs if is_valid(*x, ["+", "*"])))
    print(sum(x[0] for x in calibs if is_valid(*x, ["+", "*", "||"])))
