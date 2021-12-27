import utils
import time
import copy
import math
import re
import heapq
import numpy as np
import os
from os import path

day = 17

filename="input"+str(day)+".txt"
# filename="testinput"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    input = [l.strip() for l in f.readlines()][0] # One entry for each line
    
    # input = [x for x in input]
    # input = [int(x) for x in input[0].split(',')]
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[int(s) for s in x] for x in input]

def get_target_grid():
    [xs, ys] = input[len("target area: "):].split(", ")
    [xmin, xmax] = sorted([int(x) for x in xs[2:].split("..")])
    [ymin, ymax] = sorted([int(y) for y in ys[2:].split("..")])
    return ([xmin, xmax],[ymin, ymax])

    
def is_in_target(pos, g):
    return pos[0] >= g[0][0] and pos[0] <= g[0][1] and pos[1] >= g[1][0] and pos[1] <= g[1][1]
    
def is_past_target(pos, g):
    if pos[0] > g[0][1]:
        return True
    if pos[1] < g[1][0]:
        return True
    return False
    
    
def print_arc(pos_list, g):
    max_y = max([0] + [p[1] for p in pos_list])
    min_y = min(g[1] + [p[1] for p in pos_list])
    
    width = max(g[0][1], max([p[0] for p in pos_list]))
    height = max_y - min_y
    print(width, height)
    
    m = utils.make2dArray(width+1, height+1, ".")

    
    # max_y should end up at 0
    # min_y should be the full height
    target_min_y = -g[1][0] + max_y
    target_max_y = -g[1][1] + max_y
    print(target_min_y, target_max_y)
    for y in range(target_max_y, target_min_y+1):
        for x in range(g[0][0], g[0][1]+1):
            m[y][x] = "T"
    
    
    m[max_y][0] = "S"
    for p in pos_list:
        x = p[0]
        y = -p[1] + max_y
        
        m[y][x] = "#"
    
    last = pos_list[-1]
    m[-last[1] + max_y][last[0]] = "█"
    
    utils.printMatrix(m)
    
    
def check_velocity(x, y, g):
    # Return None if this goes past the grid
    # If it hits the grid, return the highest point we hit
    pos = (0, 0)
    
    pos_list = []
    
    max_y = 0
    
    while not is_past_target(pos, g):
        # Update the position
        pos = (pos[0] + x, pos[1] + y)
        pos_list.append(pos)
        # print(pos_list)
        
        # Set the new max if we hit it
        if pos[1] > max_y:
            max_y = pos[1]
        
        # Check if we hit the target
        if is_in_target(pos, g):
            # print_arc(pos_list, g)
            print(x, y)
            return max_y
        
        # Update the velocity
        if x > 0:
            x = x - 1
        if x < 0:
            x = x + 1
        y = y - 1
    # print_arc(pos_list, g)
    return None

def part1():
    g = get_target_grid()
    
    max_y = 0
    for x in range(0, g[0][1]+1):
        for y in range(0, -g[1][0]):
            res = check_velocity(x, y, g)
            if res and res > max_y:
                max_y = res
    
    return max_y
    
    
def part2():
    g = get_target_grid()
    
    out = 0
    for x in range(0, g[0][1]+1):
        for y in range(g[1][0]-1, -g[1][0]+1):
            res = check_velocity(x, y, g)
            if res is not None:
                out += 1
    
    return out


# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")