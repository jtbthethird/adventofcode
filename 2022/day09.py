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

day = "09"

filename="input_"+str(day)+".txt"
# filename="test_"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    input = [l.strip() for l in f.readlines()] # One entry for each line
    input = [(x.split(' ')[0], int(x.split(' ')[1])) for x in input]
    # input = f.readlines()[0].strip()
    
    # input = input.split('\n\n')
            
    # input = ["" if x == '' else int(x) for x in input]
    # input = utils.split_list(input, "")
    # input = [x for x in input]
    # input = [int(x) for x in input[0].split(',')]
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[int(s) for s in x] for x in input] # Parse a 2-d number grid


def move_T(t_pos, h_pos):
    # print("H/T", h_pos, t_pos)
    
    if abs(h_pos[0] - t_pos[0]) <= 1 and abs(h_pos[1] - t_pos[1]) <= 1:
        return t_pos

    x_move = max(min(h_pos[0] - t_pos[0], 1), -1)
    y_move = max(min(h_pos[1] - t_pos[1], 1), -1)
    # print(x_move, y_move)
        
    return (t_pos[0] + x_move, t_pos[1] + y_move)



def part1():
    
    # print(input)
    x_lookup = {'R': 1, 'L': -1, 'U': 0, 'D': 0}
    y_lookup = {'R': 0, 'L': 0, 'U': -1, 'D': 1}
    
    

    start = (0, 0)
    H_pos = start
    T_pos = start
    
    t_locs = set([T_pos])
    h_locs = set([H_pos])
    
    
    for instr in input:
        dirr = instr[0]
        for step in range(instr[1]):
            # print("-")
            # Move the head
            H_pos = (H_pos[0] + x_lookup[dirr], H_pos[1] + y_lookup[dirr])
            
            h_locs.add(H_pos)
        
            # Then move the tail
            T_pos = move_T(T_pos, H_pos)
            t_locs.add(T_pos)
            # print("ending: ", H_pos, T_pos)
            
    return len(t_locs)
    
    
def part2():
    num_knots = 10

    x_lookup = {'R': 1, 'L': -1, 'U': 0, 'D': 0}
    y_lookup = {'R': 0, 'L': 0, 'U': -1, 'D': 1}
    
    positions = [(0,0)]*num_knots
    
    t_locs = set()
    
    for instr in input:
        # print(instr)
        (dirr, steps) = instr
        for step in range(steps):
            # print(dirr)
            H_pos = positions[0]
            H_pos = (H_pos[0] + x_lookup[dirr], H_pos[1] + y_lookup[dirr])
            
            positions[0] = H_pos
            
            for n in range(1, num_knots):
                t_loc = positions[n]
                
                t_loc2 = move_T(t_loc, positions[n-1])
                positions[n] = t_loc2
            
            t_locs.add(positions[-1])
            # print(positions)
                
    return len(t_locs)

# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")