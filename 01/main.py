import sys

if __name__ == "__main__":
    filename = sys.argv[1]
    tmp = []
    with open(filename,'r') as f:
        for l in f.read().splitlines():
            a,b = l.split()
            tmp.append([int(a),int(b)])

    # transpose
    lists = list(zip(*tmp))
    # sort and transpose back
    sorted_lists = list(zip(*(sorted(l) for l in lists)))
    dist = sum(abs(b-a) for a,b in sorted_lists)
    print(dist)
    

