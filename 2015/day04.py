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

day = "04"

filename="input_"+str(day)+".txt"
# filename="test_"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    # input = [x for x in f.readlines()[0]]
    input = f.readlines()[0].strip() # One liner entry
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
    
    num = 0
    while True:
        key = "%s%d"%(input, num)
        val = hashlib.md5(key.encode('ascii')).hexdigest()
        if val[:5] == '00000':
            print(val, key)
            return num
        num = num + 1
    return 0
        
    
def part2():
    
    num = 0
    while True:
        key = "%s%d"%(input, num)
        val = hashlib.md5(key.encode('ascii')).hexdigest()
        if val[:6] == '000000':
            print(val, key)
            return num
        num = num + 1
    return 0
    
    return 0
            

# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")