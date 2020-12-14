import template
import copy
import re

filename="input6.txt"
# filename="testinput5.txt"

input = []
with open(filename) as f:
    input = f.read()
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[s for s in x] for x in input]
 
 
# --- #
def part1():
    person = [p for p in g for g in [p.split('\n') for p in input.split('\n\n')]]
    result = []
    for group in groups:
        s = set()
        for person in group:
            t = [m for m in person]
            for l in t:
                s.add(l)
        result.append(len(s))
    return sum(result)
    
def part2():
    groups = [p.split('\n') for p in input.split('\n\n')]
    result = []
    for group in groups:
        s = set()
        [s.add(l) for l in group[0]]
        for p in group[1:]:
            pl = [l for l in p]
            slist = list(s)
            [s.remove(l) for l in slist if l not in pl]
        result.append(len(s))
    return sum(result)

# --- #

if __name__ == "__main__":
    template.funWrapper(part1, "Part 1")
    template.funWrapper(part2, "Part 2")