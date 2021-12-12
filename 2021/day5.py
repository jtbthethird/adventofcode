import utils
import copy
import re
import numpy as np
from os import path

day = 5

filename="input"+str(day)+".txt"
# filename="testinput"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []
with open(filepath) as f:
    input = [l.strip() for l in f.readlines()] # One entry for each line
    
    # input = [x for x in input]
    
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[int(s) for s in x] for x in input]

lines = []
for row in input:
    [s, arrow, e] = row.split()
    lines.append([[int(p) for p in s.split(",")], [int(p) for p in e.split(",")]])

max_x = max([point[0] for line in lines for point in line])
max_y = max([point[1] for line in lines for point in line])

# print(max_x, max_y)

vent_map = [ [0] * (max_x+1) for _ in range(max_y+1) ]

# utils.printMatrix(vent_map)

def add_line_to_map(vmap, line):
    [p0, p1] = line
    if p0[0] == p1[0]:
        # Vertical line
        x = p0[0]
        y1 = p0[1]
        y2 = p1[1]
        for y in range(min(y1, y2), max(y1, y2)+1):
            # print("Updating %d, %d"%(x, y))
            vmap[y][x] += 1
    elif p0[1] == p1[1]:
        y = p0[1]
        x1 = p0[0]
        x2 = p1[0]
        for x in range(min(x1, x2), max(x1, x2)+1):
            # print("Updating %d, %d"%(x, y))
            vmap[y][x] += 1
    else:
        if p0[0] < p1[0]:
            left = p0
            right = p1
        else:
            left = p1
            right = p0
            
        # print("updating line from ", left, right)
        
        y_inc = 1
        if right[1] < left[1]:
            y_inc = -1
        for i in range(right[0] - left[0] + 1):
            x = left[0] + i
            y = left[1] + (i * y_inc)
            # print("Updating %d, %d"%(x, y))
            vmap[y][x] += 1
        
    
    return vmap
    
    

def part1():
    vmap = copy.deepcopy(vent_map)
    for line in lines:
        [p0, p1] = line
        print()
        print("Checking line: ", p0, p1)
        if (p0[0] != p1[0] and p0[1] != p1[1]):
            # print("Diagonal of some kind")
            continue
        else:
            # Add this to the map
            vmap = add_line_to_map(vmap, line)


    utils.printMatrix(vmap)
    
    vals = [val for row in vmap for val in row]
    

    return sum([1 if t > 1 else 0 for t in vals])
            
            
    
def part2():
    vmap = copy.deepcopy(vent_map)
    for line in lines:
        [p0, p1] = line
        print()
        print("Checking line: ", p0, p1)
        vmap = add_line_to_map(vmap, line)


    utils.printMatrix(vmap)
    
    vals = [val for row in vmap for val in row]
    

    return sum([1 if t > 1 else 0 for t in vals])
    

# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")