import template
import copy
import re

filename="input9.txt"
# filename="testinput9.txt"

input = []
with open(filename) as f:
    input = f.readlines()
    input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[s for s in x] for x in input]

# --- #
def part1():
    sRange = 25
        
    preamble = input[:sRange]
    

    # p = [(x + y) for i, x in enumerate(preamble) for y in preamble[i+1:]]
    # print(p)

    d = {
        x: [y+x for y in preamble[i+1:]] for (i,x) in enumerate(preamble)
    }
    
    for i,v in enumerate(input[sRange:]):
        z = set([y for x in d.values() for y in x])
        
        # print("looping round %d val %d"%(i,v))
        # print("dict: ", d)
        # print("set: ", z)
        
        valid = v in z
        if not valid:
            print("invalid!")
            return v
        removed = d.pop(input[i])
        for k in d:
            d[k].append(k + v)
        d[v] = []
    
    return -1
    
def part2():
    val_to_find = 15690279
    # val_to_find = 127

    print(input)
    
    for lo in range(len(input)):
        # print("Lo: ", lo)
        for hi in range(lo+1, len(input)):
            # print("hi: ", hi)
            r = input[lo:hi]
            val = sum(r)
            if val == val_to_find:
                print("Match", lo, hi, r, min(r), max(r))
                return min(r) + max(r)
            if val > val_to_find:
                print("too big: ", input[lo:hi], val)
                break
    
    return 2
    

# --- #

if __name__ == "__main__":
    template.funWrapper(part1, "Part 1")
    template.funWrapper(part2, "Part 2")
