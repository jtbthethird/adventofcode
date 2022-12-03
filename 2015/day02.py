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

day = "02"

filename="input_"+str(day)+".txt"
# filename="test_"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    input = [l.strip() for l in f.readlines()] # One entry for each line
    input = [sorted([int(x) for x in y.split('x')]) for y in input]
    
    # input = [x for x in input[0]]
    # input = ["" if x == '' else int(x) for x in input]
    # input = utils.split_list(input, "")
    # input = [x for x in input]
    # input = [int(x) for x in input[0].split(',')]
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[int(s) for s in x] for x in input]

def area_for_present(present):
    base = 2 * present[0] * present[1] + 2 * present[1] * present[2] + 2 * present[2] * present[0]
    
    slack = present[0] * present[1]
    
    return base + slack

def part1():
    return sum([area_for_present(x) for x in input])


def ribbon_length(present):
    length =  (2 * present[0] + 2 * present[1]) + (present[0] * present[1] * present[2])
    # print(present, length)
    return length
    
def part2():
    return sum([ribbon_length(x) for x in input])
    


# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")