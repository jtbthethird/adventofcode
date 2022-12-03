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
    
    input = [x.split(' ') for x in input]
    # input = ["" if x == '' else int(x) for x in input]
    # input = utils.split_list(input, "")
    # input = [x for x in input]
    # input = [int(x) for x in input[0].split(',')]
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[int(s) for s in x] for x in input]



#
# A, X = Rock
# B, Y = Paper
# C, Z = Scissors

# lose = 0
# win  = 6
# draw = 3

def get_result(theirs, mine):
    
    
    outcome_map = { "A": {"X": 3, "Y": 6, "Z": 0}, 
                    "B": {"X": 0, "Y": 3, "Z": 6}, 
                    "C": {"X": 6, "Y": 0, "Z": 3}, }
    my_score_map = {"X": 1, "Y": 2, "Z": 3}
    
    return outcome_map[theirs][mine] + my_score_map[mine]


def part1():
    # print(input)
    
    scores = [get_result(row[0], row[1]) for row in input]
        
    # print(scores)

    return sum(scores)

# A = Rock
# B = Paper
# C = Scissors

# X = Lose
# Y = Draw
# Z = Win

def pick_throw(theirs, result):
    my_throw_map = { "A": {"X": "Z", "Y": "X", "Z": "Y"}, 
                    "B": {"X": "X", "Y": "Y", "Z": "Z"}, 
                    "C": {"X": "Y", "Y": "Z", "Z": "X"} }
                    

                    
    return get_result(theirs, my_throw_map[theirs][result])
    
def part2():
    scores = [pick_throw(row[0], row[1]) for row in input]

    return sum(scores)

# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")