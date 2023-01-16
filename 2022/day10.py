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

day = "10"

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
    # input = [int(x) for x in input[0].split(',')]
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[int(s) for s in x] for x in input] # Parse a 2-d number grid


def do_step(instr, history):
    if instr == 'noop':
        history.append(history[-1])
        return
        
    
    [name, val] = instr.split(' ')
    if name != 'addx':
        print("FAILURE")
        throw
    
    history.append(history[-1])
    history.append(history[-1] + int(val))
    
    return


def part1():    
    history = [1]
    
    for step in input:
        do_step(step, history)
            
        # print(history)
    
    ids = [20, 60, 100, 140, 180, 220]
        
    
    t = [history[i-1]*i for i in ids]
    
    # print(t)
    
    return sum(t)
    
    
def part2():
    
    arr = utils.make2dArray(40, 6, ' ')
    
    history = [1]
    for step in input:
        do_step(step, history)
    
    for i in range(1, 241):
        sprite_pos = history[i-1]
        
        x = (i-1) % 40
        y = math.floor((i-1) / 40)
        
        # print(i, x, y)
        
        if abs(sprite_pos-x) <= 1:
            # print("hit")
            arr[y][x] = '*'
        
    utils.printMatrix(arr)
    
    return 0
    
# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")