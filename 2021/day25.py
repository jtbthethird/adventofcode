import utils
import time
import copy
import math
import re
import heapq
import numpy as np
import os
from collections import Counter
from os import path

day = 25

filename="input"+str(day)+".txt"
# filename="testinput"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    input = [l.strip() for l in f.readlines()] # One entry for each line
    
    input = [list(r) for r in input]
    # input = [x for x in input]
    # input = [int(x) for x in input[0].split(',')]
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[int(s) for s in x] for x in input]

def mat_to_str(matrix):
    return "".join(["".join(row) for row in matrix])

def do_step(grid):
    east_step = copy.deepcopy(grid)
    did_move = False
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            right = (x+1) % len(row)
            right_val = row[right]
            if val == ">" and right_val == ".":
                east_step[y][x] = "."
                east_step[y][right] = ">"
                did_move = True

    out = copy.deepcopy(east_step)
    for y, row in enumerate(east_step):
        for x, val in enumerate(row):
            down = (y+1) % len(grid)
            down_val = east_step[down][x]
            if val == "v" and down_val == ".":
                out[y][x] = "."
                out[down][x] = "v"
                did_move = True
    return (did_move, out)
    

def part1():
    utils.printMatrix(input)
    
    grid = copy.copy(input)
    
    did_move = True
    i = 0
    while did_move:

        i += 1
        (did_move, grid) = do_step(grid)
    print()
    print(i)
    utils.printMatrix(grid)
    
    return i
    
    
def part2():
    return 0

# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")