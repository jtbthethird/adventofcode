import utils
import time
import string
import copy
import math
import re
import heapq
import numpy as np
import os
from collections import Counter
from os import path

day = "04"

filename="input_"+str(day)+".txt"
# filename="test_"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    input = [l.strip() for l in f.readlines()] # One entry for each line
    
    assignments = [[[int(v) for v in e.split('-')] for e in line.split(',')] for line in input]
    # print(assignments)
            
    # input = ["" if x == '' else int(x) for x in input]
    # input = utils.split_list(input, "")
    # input = [x for x in input]
    # input = [int(x) for x in input[0].split(',')]
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[int(s) for s in x] for x in input]


def part1():
    total = 0
    for pair in assignments:
        [a, b] = pair
        if (a[0] >= b[0] and a[1] <= b[1]) or (a[0] <= b[0] and a[1] >= b[1]):
            total += 1
    return total
    
    
def part2():
    total = 0
    for pair in assignments:
        [a, b] = pair
        if (a[0] <= b[1] and a[1] >= b[0]):
            total += 1
    return total


# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")