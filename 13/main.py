import sys
import numpy as np


def cost(a, b, prize):
    det = a[0] * b[1] - a[1] * b[0]
    if det == 0:
        return 0

    vec = np.array([[b[1], -b[0]], [-a[1], a[0]]]).dot(prize)

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
        sum(
            cost(
                A_vecs[i],
                B_vecs[i],
                X_vecs[i],
            )
            for i in range(len(A_vecs))
        ),
        sum(
            cost(
                A_vecs[i],
                B_vecs[i],
                X_vecs[i] + np.array([10000000000000, 10000000000000]),
            )
            for i in range(len(A_vecs))
        ),
    )
