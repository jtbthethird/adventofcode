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

day = "03"

filename="input_"+str(day)+".txt"
# filename="test_"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    input = [l.strip() for l in f.readlines()] # One entry for each line
    
    # input = ["" if x == '' else int(x) for x in input]
    # input = utils.split_list(input, "")
    # input = [x for x in input]
    # input = [int(x) for x in input[0].split(',')]
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[int(s) for s in x] for x in input]


def part1():
    alph = string.ascii_lowercase + string.ascii_uppercase
    s = 0
    for line in input:
        half = int(len(line)/2)
        first = set([x for x in line[:half]])
        second = set([x for x in line[half:]])
        d = first.intersection(second)
        c = next(iter(d))
        o = alph.index(c) + 1
        # print(d, c, o)
        s += o
    return s

    
    
def part2():
    alph = '0' + string.ascii_lowercase + string.ascii_uppercase


    outs = []
    for i in range(0, len(input), 3):
        a = set([x for x in input[i]])
        b = set([x for x in input[i+1]])
        c = set([x for x in input[i+2]])
        
        i = next(iter(a.intersection(b).intersection(c)))
        print(i)
        outs.append(i)

    
    return sum([alph.index(x) for x in outs])


# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")