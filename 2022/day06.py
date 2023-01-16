import utils
import time
import string
import copy
import math
import re
import heapq
import numpy as np
import os
from collections import Counter, defaultdict
from os import path

day = "06"

filename="input_"+str(day)+".txt"
# filename="test_"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    # input = [l.strip() for l in f.readlines()] # One entry for each line
    input = f.readlines()[0].strip()
    
    # input = input.split('\n\n')
            
    # input = ["" if x == '' else int(x) for x in input]
    # input = utils.split_list(input, "")
    # input = [x for x in input]
    # input = [int(x) for x in input[0].split(',')]
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[int(s) for s in x] for x in input]


# --- Parse the inputs ---


def part1():
    for i in range(4, len(input)):
        # print(input[i-4:i])
        if len(set(input[i-4:i])) == 4:
            return i
    
    return 0
    
    
def part2():
    for i in range(14, len(input)):
        # print(input[i-14:i])
        if len(set(input[i-14:i])) == 14:
            return i
    return 0


# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")