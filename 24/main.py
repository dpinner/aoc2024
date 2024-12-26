import sys
from collections import defaultdict, deque
from typing import Dict, Set, List, Tuple

op_map = {
    "AND": lambda v1, v2: v1 & v2,
    "OR": lambda v1, v2: v1 | v2,
    "XOR": lambda v1, v2: v1 ^ v2,
}


# def evaluate(q: deque, vals: Dict[str, int]):
#     while q:
#         var1, op, var2, out = q.popleft()
#         if var1 not in vals or var2 not in vals:
#             q.append((var1, op, var2, out))
#             continue
#         vals[output] = op_map[op](vals[var1], vals[var2])


def evaluate(q: List[str], eqns: Dict[str, Tuple[str, str, str]], vals: Dict[str, int]):
    for var in q:
        if var in vals:
            continue

        dep1, op, dep2 = eqns[var]
        vals[var] = op_map[op](vals[dep1], vals[dep2])


def load(var: str, q: List[str], visited: Set[str], deps: Dict[str, Set[str]]):
    if var in visited:
        return

    for child in deps.get(var, set()):
        load(child, q, visited, deps)

    q.append(var)
    visited.add(var)


def part1(
    deps: Dict[str, Set[str]],
    eqns: Dict[str, Tuple[str, str, str]],
    vals: Dict[str, int],
) -> int:
    q = []
    seen = set()
    for var, dep_set in sorted(deps.items(), key=lambda x: len(x[1])):
        load(var, q, seen, deps)

    evaluate(q, eqns, vals)

    z = "".join(
        [
            str(val)
            for var, val in sorted(vals.items(), reverse=True)
            if var.startswith("z")
        ]
    )

    return int(z, 2)


def part2(eqns: Dict[str, Tuple[str, str, str]]):
    rev_eqns = {}
    for k, v in eqns.items():
        rev_eqns[v] = k
        var1, op, var2 = v
        rev_eqns[(var2, op, var1)] = k

    swaps = []

    print(rev_eqns[("x00", "XOR", "y00")])
    if rev_eqns[("x00", "XOR", "y00")] != "z00":
        swaps.append("z00")
        swaps.append(rev_eqns[("x00", "XOR", "y00")])

    prev_carry = rev_eqns[("x00", "AND", "y00")]
    for i in range(1, 45):
        x = f"x0{i}" if i < 10 else f"x{i}"
        y = f"y0{i}" if i < 10 else f"y{i}"
        z = f"z0{i}" if i < 10 else f"z{i}"
        sum_int = rev_eqns[(x, "XOR", y)]
        carry_int = rev_eqns[(x, "AND", y)]
        c1 = rev_eqns[(prev_carry, "AND", sum_int)]
        if rev_eqns[(sum_int, "XOR", prev_carry)] != z:
            swaps.append(z)
            v = rev_eqns[(sum_int, "XOR", prev_carry)]
            swaps.append(v)
            rev_eqns[(sum_int, "XOR", prev_carry)] = z
            rev_eqns[(prev_carry, "XOR", sum_int)] = z
            vv1, op, vv2 = eqns[z]
            rev_eqns[(vv1, op, vv2)] = v
            rev_eqns[(vv2, op, vv1)] = v
            print(swaps)
        print(rev_eqns[(sum_int, "XOR", prev_carry)])

        prev_carry = rev_eqns[(c1, "OR", carry_int)]

    print(rev_eqns[("x44", "AND", "y44")])


def swap(a, b, outputs, eqns):
    v1, op, v2 = eqns[a]
    outputs[(v1, op, v2)] = b
    outputs[(v2, op, v1)] = b
    v1, op, v2 = eqns[b]
    outputs[(v1, op, v2)] = a
    outputs[(v2, op, v1)] = a


def validate(i, prev_carry, eqns, pairs, swaps, locked):
    if i == 45:
        return
    swap_map = {}
    for a, b in swaps:
        swap_map[a] = b
        swap_map[b] = a
    outputs = {}
    for k, v in eqns.items():
        outputs[v] = swap_map.get(k, k)
        var1, op, var2 = v
        outputs[(var2, op, var1)] = swap_map.get(k, k)

    x = f"x0{i}" if i < 10 else f"x{i}"
    y = f"y0{i}" if i < 10 else f"y{i}"
    z = f"z0{i}" if i < 10 else f"z{i}"

    w = outputs[(x, "XOR", y)]

    if (w, "XOR", prev_carry) not in outputs:
        if (w, "XOR") in pairs:
            swaps.append((prev_carry, pairs[(w, "XOR")]))
            swap(prev_carry, pairs[(w, "XOR")], outputs, eqns)
        else:
            swaps.append((w, pairs[(prev_carry, "XOR")]))
            swap(w, pairs[(prev_carry, "XOR")], outputs, eqns)
    elif outputs[(w, "XOR", prev_carry)] != z:
        swaps.append((z, outputs[(w, "XOR", prev_carry)]))
        swap(z, outputs[(w, "XOR", prev_carry)], outputs, eqns)

    w = outputs[(x, "XOR", y)]

    if (w, "AND", prev_carry) not in outputs:
        # not sure what to do here, can't obviously swap any of these
        print(i, "missing (x ^ y) . c_prev -- have (x ^ y) .", pairs[(w, "AND")])
        return

    q = outputs[(x, "AND", y)]
    u = outputs[(w, "AND", prev_carry)]
    if (q, "OR", u) not in outputs:
        if (q, "OR") in pairs:
            swaps.append((u, pairs[(q, "OR")]))
            swap(u, pairs[(q, "OR")], outputs, eqns)
        else:
            swaps.append((q, pairs[(u, "OR")]))
            swap(q, pairs[(u, "OR")], outputs, eqns)

    if i == 44:
        print("carry ==", outputs[(q, "OR", u)])
    validate(i + 1, outputs[(q, "OR", u)], eqns, pairs, swaps, locked)


if __name__ == "__main__":
    filename = sys.argv[1]
    vals = {}
    deps: Dict[str, Set[str]] = defaultdict(set)
    eqns: Dict[str, Tuple[str, str, str]] = {}
    pairs: Dict[Tuple[str, str], str] = {}
    with open(filename, "r") as f:
        for line in f:
            if len(line.rstrip().split(":")) > 1:
                var, val = line.rstrip().split(":")
                vals[var] = int(val.strip())

            if len(line.rstrip().split(" -> ")) > 1:
                eqn, output = line.rstrip().split(" -> ")
                var1, op, var2 = eqn.split()
                deps[output].add(var1)
                deps[output].add(var2)
                eqns[output] = (var1, op, var2)
                pairs[(var1, op)] = var2
                pairs[(var2, op)] = var1

    print(part1(deps, eqns, vals))

    swaps = []
    validate(1, "brj", eqns, pairs, swaps, set())

    print(",".join(sorted(sum(swaps, ()))))
