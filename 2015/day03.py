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

day = "03"

filename="input_"+str(day)+".txt"
# filename="test_"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    input = [x for x in f.readlines()[0]]
    # input = [l.strip() for l in f.readlines()] # One entry for each line
    # input = [sorted([int(x) for x in y.split('x')]) for y in input]
    
    # input = [x for x in input[0]]
    # input = ["" if x == '' else int(x) for x in input]
    # input = utils.split_list(input, "")
    # input = [x for x in input]
    # input = [int(x) for x in input[0].split(',')]
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[int(s) for s in x] for x in input]

def part1():
    print(input)
    pos = (0,0)
    
    d = {pos: 1}
        
    for direction in input:
        p1 = pos
        if direction == '>':
            p1 = (pos[0] + 1, pos[1])
        elif direction == '<':
            p1 = (pos[0] - 1, pos[1])
        elif direction == 'v':
            p1 = (pos[0], pos[1] + 1)
        elif direction == '^':
            p1 = (pos[0], pos[1] - 1)
        if p1 in d:
            d[p1] = d[p1] + 1
        else:
            d[p1] = 1
        pos = p1
        # print(d)
    
    out = [y for y in d.items() if y[1] >= 1]
    
    return len(out)
        
    
def part2():
    posA = (0,0)
    posB = (0,0)
    
    houses = set([posA])
    
    for i, direction in enumerate(input):
        p = posA
        if i % 2 == 1:
            p = posB
            
        # print("\n\n\n", i, direction, p)
        
        if direction == '>':
            p = (p[0] + 1, p[1])
        elif direction == '<':
            p = (p[0] - 1, p[1])
        elif direction == 'v':
            p = (p[0], p[1] + 1)
        elif direction == '^':
            p = (p[0], p[1] - 1)
        
        houses.add(p)
        
        if i % 2 == 1:
            posB = p
        else:
            posA = p
    
    # print(houses)
    
    return len(houses)
            

# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")