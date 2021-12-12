import template
import copy
import re



filename="input10.txt"
# filename="testinput10.txt"

input = []
with open(filename) as f:
    input = f.readlines()
    input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[s for s in x] for x in input]

# --- #
def part1():
    diffs = [0,0,0,0]
    data = copy.copy(input)
    
    data.sort()
    data.append(data[-1]+3)
    last = 0
    for i, v in enumerate(data):
        diff = v - last
        diffs[diff] += 1
        last = v

    print(diffs)
    return (diffs[1] * diffs[3])

def part2():
    data = copy.copy(input)
    
    data.sort()
    data.append(data[-1]+3)
    data.reverse()
    data.append(0)
    
    paths = {}
    paths[data[0]] = 1
    last = data[0]
    
    for j, v in enumerate(data[1:]):
        diff = last - v
        if diff == 3:
            paths[v] = paths[last]
        else:
            q = sum([paths[p] for p in [x for x in data[max(0, j-2):j+1] if x-v <= 3]])
            paths[v] = q
        last = v
    return paths[0]
        

if __name__ == "__main__":
    template.funWrapper(part1, "Part 1")
    template.funWrapper(part2, "Part 2")
