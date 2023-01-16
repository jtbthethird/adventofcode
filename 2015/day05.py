import utils
import time
import copy
import math
import re
import heapq
import numpy as np
import os
import hashlib
from collections import Counter
from os import path

day = "05"

filename="input_"+str(day)+".txt"
# filename="test_"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    # input = [x for x in f.readlines()[0]]
    # input = f.readlines()[0].strip() # One liner entry
    input = [l.strip() for l in f.readlines()] # One entry for each line
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
    # print(input)
    nice_words = []
    
    for line in input:
        # print("\n----\n", line)
        
        vowels = re.search(r"[aeiou].*[aeiou].*[aeiou]", line) is not None
        double_letter = re.search(r"(.)\1", line) is not None
        bad_word = False
        for x in ['ab', 'cd', 'pq', 'xy']:
            if x in line:
                bad_word = True
                break
        
        if vowels and double_letter and not bad_word:
            # print("NICE")
            nice_words.append(line)
        
    return len(nice_words)
        
    
def part2():
    count = 0
    
    for line in input:
        # print("\n", line)
        
        doubles = re.search(r"(..).*\1", line)
        sammy = re.search(r"(.).\1", line)
            
        if doubles and sammy:
            count = count + 1
    return count
            

# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")