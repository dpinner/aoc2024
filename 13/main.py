import sys
import numpy as np


def cost(a, b, prize, offset=None):
    det = a[0] * b[1] - a[1] * b[0]
    if det == 0:
        return 0

    target = prize if offset is None else prize + offset

    vec = np.array([[b[1], -b[0]], [-a[1], a[0]]]).dot(target)

    if any(v % det != 0 for v in vec):
        return 0
    return np.array([3, 1]).dot(vec) // det


if __name__ == "__main__":
    filename = sys.argv[1]
    A_vecs = []
    B_vecs = []
    X_vecs = []
    with open(filename, "r") as f:
        for line in f:
            if not line:
                continue
            split_line = line.rstrip().split(":")
            if split_line[0] != "" and split_line[0][-1] == "A":
                A_vecs.append(
                    [int(x.split("+")[-1]) for x in split_line[-1].split(",")]
                )
            if split_line[0] != "" and split_line[0][-1] == "B":
                B_vecs.append(
                    [int(x.split("+")[-1]) for x in split_line[-1].split(",")]
                )
            if split_line[0] == "Prize":
                X_vecs.append(
                    [int(x.split("=")[-1]) for x in split_line[-1].split(",")]
                )

    print(
        sum(cost(*vecs) for vecs in zip(A_vecs, B_vecs, X_vecs)),
        sum(
            cost(*vecs, offset=np.array([10000000000000, 10000000000000]))
            for vecs in zip(A_vecs, B_vecs, X_vecs)
        ),
    )
