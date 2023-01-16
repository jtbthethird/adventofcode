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
import functools
import operator
import json

day = "13"

filename="input_"+str(day)+".txt"
# filename="test_"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    input = [l.strip() for l in f.readlines()] # One entry for each line
    # input = [(x.split(' ')[0], int(x.split(' ')[1])) for x in input]
    # input = f.readlines()[0].strip()
    
    # input = input.split('\n\n')
            
    # input = ["" if x == '' else int(x) for x in input]
    # input = utils.split_list(input, "")
    # input = [x for x in input]
    # input = [int(x) for x in input[0].split('')]
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[int(s) for s in x] for x in input] # Parse a 2-d number grid


def check_list(a, b):
    
    a_len = len(a)
    b_len = len(b)
    
    for i in range(min(a_len, b_len)):
        x = a[i]
        y = b[i]
        # print("checking ", x, y)
        if isinstance(x, int) and isinstance(y, int):
            # print("Both ints")
            if x == y:
                # print(x, y, "equal")
                continue
            if x < y:
                # print(x, y, "smaller")
                return 1
            if x > y:
                # print(x, y, "greater")
                return -1
        elif isinstance(x, list) and isinstance(y, list):
            list_result = check_list(x, y)
            if list_result == -1:
                # print("no good")
                return -1
            elif list_result == 1:
                # print("found right order.")
                return 1
            else:
                # print("list is good. Keep going")
                continue
        else:
            # print("mismatch")
            if isinstance(x, list):
                y = [y]
            else:
                x = [x]
            list_result = check_list(x, y)
            if list_result == -1:
                # print("no good")
                return -1
            elif list_result == 1:
                # print("found right order.")
                return 1
            else:
                # print("list is good. Keep going")
                continue
            
    # Got to the end
    # print("End: ", a_len, b_len)
    if a_len == b_len:
        return 0
    elif b_len < a_len:
        return -1
    else:
        return 1
    
    return 0


def part1():
    out = []
    pairs = utils.split_list(input, "")
    
    for i, pair in enumerate(pairs):
        (a, b) = pair
    
        a2 = json.loads(a)
        b2 = json.loads(b)
        
        x = check_list(a2, b2)
        
        if x >= 0:
            out.append(i+1)
    
    
    return sum(out)

    
    
def part2():
    divider1 = [[2]]
    divider2 = [[6]]
    
    
    
    
    packets = [json.loads(x) for x in input if x != '']
    packets.append(divider1)
    packets.append(divider2)
    
    print(packets)
    
    packets = sorted(packets, key=functools.cmp_to_key(check_list), reverse=True)
    print(packets)
    
    
    
    return (1+packets.index(divider1)) * (1+packets.index(divider2))
    
# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")