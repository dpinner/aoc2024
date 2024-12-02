import sys
from typing import List


def is_safe(max_diff: int, min_diff: int) -> bool:
    return (min_diff * max_diff > 0) and (
        (max_diff <= 3 and min_diff >= 1) or (max_diff <= -1 and min_diff >= -3)
    )


def safe_report(report: List[int]) -> bool:
    diffs = [a - b for a, b in zip(report, report[1:])]
    return is_safe(max(diffs), min(diffs))


if __name__ == "__main__":
    filename = sys.argv[1]
    reports = []
    with open(filename, "r") as f:
        for l in f.read().splitlines():
            levels = list(map(int, l.split()))
            reports.append(levels)

    print(sum(safe_report(r) for r in reports))
    print(
        sum(
            safe_report(r)
            or any(safe_report(r[:i] + r[i + 1 :]) for i in range(len(r)))
            for r in reports
        )
    )
