import sys
import re
from typing import List


def mul(terms: List[str]) -> int:
    x, y = 0, 0
    enabled = True
    for term in terms:
        if term == "do()":
            enabled = True
            continue
        if term == "don't()":
            enabled = False
            continue
        nums = list(map(int, re.findall(r"\d{1,3}", term)))
        x += nums[0] * nums[1]
        if enabled:
            y += nums[0] * nums[1]
    return x, y


if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename, "r") as f:
        str = f.read()

    terms = re.findall(r"do\(\)|mul\(\d{1,3},\d{1,3}\)|don't\(\)", str)

    print(mul(terms))
