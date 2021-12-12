import utils
import copy
import re
import numpy as np
from os import path

day = 9

filename="input"+str(day)+".txt"
# filename="testinput"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    input = [l.strip() for l in f.readlines()] # One entry for each line
    
    # input = [x for x in input]
    # input = [int(x) for x in input[0].split(',')]
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    input = [[int(s) for s in x] for x in input]
    

def part1():
    m = copy.deepcopy(input)
    utils.printMatrix(input)
    low_scores = []
    for y, row in enumerate(m):
        for x, val in enumerate(row):
            borders = []
            if x > 0:
                borders.append(row[x-1])
            if x + 1 < len(row):
                borders.append(row[x+1])
            if y > 0:
                borders.append(m[y-1][x])
            if y + 1 < len(m):
                borders.append(m[y+1][x])
            if all(b > val for b in borders):
                print(x, y, val, borders)
                print("--- low point --- ")
                low_scores.append(val + 1)
    return sum(low_scores)

def get_basin_size(low_point, m):
    basin_size = 0
    lp = (low_point[0], low_point[1])
    points_to_check = set([lp])
    checked = set()
        
    while len(points_to_check) > 0:
        cp = points_to_check.pop()
        # print("popped: ", cp, points_to_check)
        checked.add(cp)
        if m[cp[1]][cp[0]] == 9:
            # print("it's 9")
            continue
        basin_size += 1
        if cp[0] > 0:
            left = (cp[0]-1, cp[1])
            if left not in points_to_check and left not in checked:
                points_to_check.add(left)
        if cp[0] + 1 < len(m[0]):
            right = (cp[0]+1, cp[1])
            if right not in points_to_check and right not in checked:
                points_to_check.add(right)
        if cp[1] > 0:
            up = (cp[0], cp[1]-1)
            if up not in points_to_check and up not in checked:
                points_to_check.add(up)
        if cp[1] + 1 < len(m):
            down = (cp[0], cp[1]+1)
            if down not in points_to_check and down not in checked:
                points_to_check.add(down)
    print("---- Basin size ----")
    print(low_point, basin_size)
    print()
    return basin_size
    
def part2():
    m = copy.deepcopy(input)
    utils.printMatrix(input)
    low_points = []
    for y, row in enumerate(m):
        for x, val in enumerate(row):
            borders = []
            if x > 0:
                borders.append(row[x-1])
            if x + 1 < len(row):
                borders.append(row[x+1])
            if y > 0:
                borders.append(m[y-1][x])
            if y + 1 < len(m):
                borders.append(m[y+1][x])
            if all(b > val for b in borders):
                # print(x, y, val, borders)
                # print("--- low point --- ")
                low_points.append([x,y])
    print(low_points)
    basins = [get_basin_size(p, m) for p in low_points]
    basins.sort()
    basins.reverse()
    print(basins)
    
    return basins[0] * basins[1] * basins[2]
        
    

# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")