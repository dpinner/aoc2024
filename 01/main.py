import sys
from collections import defaultdict
from typing import Iterator, List, Tuple

def get_dist(input: Tuple[Tuple[int,...], Tuple[int,...]]) -> int:
    # sort and transpose back
    sorted_lists = zip(*(sorted(l) for l in input))
    return sum(abs(b-a) for a,b in sorted_lists)

def get_similarity(input: Tuple[Tuple[int,...], Tuple[int,...]]) -> int:
    freqs = defaultdict(int)
    for v in input[1]:
        freqs[v] += 1
    return sum(v * freqs[v] for v in input[0])

if __name__ == "__main__":
    filename = sys.argv[1]
    tmp = []
    with open(filename,'r') as f:
        for l in f.read().splitlines():
            a,b = l.split()
            tmp.append((int(a),int(b)))
    
    # transpose
    lists = tuple(zip(*tmp))

    # part 1
    print(get_dist(lists))

    # part 2
    print(get_similarity(lists))
    

