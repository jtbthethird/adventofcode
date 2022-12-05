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

day = "05"

filename="input_"+str(day)+".txt"
# filename="test_"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    # input = [l.strip() for l in f.readlines()] # One entry for each line
    input = [l.rstrip('\n') for l in f.readlines()]
    
    # input = input.split('\n\n')
            
    # input = ["" if x == '' else int(x) for x in input]
    input = utils.split_list(input, "")
    # input = [x for x in input]
    # input = [int(x) for x in input[0].split(',')]
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[int(s) for s in x] for x in input]


# --- Parse the inputs ---
num_columns = int(input[0][-1].strip().split(' ')[-1])
cols = defaultdict(lambda: [])
for line in input[0][:-1]:
    for i in range(num_columns):
        if line[i*4+1] != " ":
            cols[i+1].append(line[i*4+1])

instructions = [[int(x) for x in re.match(r"move (\d+) from (\d+) to (\d+)", line).groups()] for line in input[1]]
# print(instructions)

def part1():
    columns = copy.copy(cols)
    for inst in instructions:
        # print('\n\n')
        # print(columns.items())
        # print(inst)
        [num_to_move, from_stack, to_stack] = inst
        crates, remaining = columns[from_stack][:num_to_move], columns[from_stack][num_to_move:]
        # print(crates, remaining)
        crates.reverse()
        columns[from_stack] = remaining
        columns[to_stack] = crates + columns[to_stack]
        # print(columns.items())
    tops = [x[1][0] for x in sorted(columns.items(), key=lambda x: x[0])]
    return ''.join(tops)
    
    
def part2():
    columns = copy.copy(cols)
    for inst in instructions:
        # print('\n\n')
        # print(columns.items())
        # print(inst)
        [num_to_move, from_stack, to_stack] = inst
        crates, remaining = columns[from_stack][:num_to_move], columns[from_stack][num_to_move:]
        # print(crates, remaining)
        # crates.reverse()
        columns[from_stack] = remaining
        columns[to_stack] = crates + columns[to_stack]
        # print(columns.items())
    tops = [x[1][0] for x in sorted(columns.items(), key=lambda x: x[0])]
    return ''.join(tops)


# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")