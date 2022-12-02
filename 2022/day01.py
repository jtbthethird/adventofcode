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

day = "01"

filename="input_"+str(day)+".txt"
# filename="test_"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    input = [l.strip() for l in f.readlines()] # One entry for each line
    
    input = ["" if x == '' else int(x) for x in input]
    input = utils.split_list(input, "")
    # input = [x for x in input]
    # input = [int(x) for x in input[0].split(',')]
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[int(s) for s in x] for x in input]


def part1():
    max_cals = 0
    for elf in input:
        elf_val = sum(elf)
        if elf_val > max_cals:
            max_cals = elf_val
    return max_cals

    
    
def part2():
    elf_counts = []
    for elf in input:
        elf_counts.append(sum(elf))
    
    print(elf_counts)
    elf_counts.sort()
    elf_counts.reverse()
    print(elf_counts)
    
    return sum(elf_counts[:3])


# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")