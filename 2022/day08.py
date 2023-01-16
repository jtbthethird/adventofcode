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

day = "08"

filename="input_"+str(day)+".txt"
# filename="test_"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    input = [l.strip() for l in f.readlines()] # One entry for each line
    # input = f.readlines()[0].strip()
    
    # input = input.split('\n\n')
            
    # input = ["" if x == '' else int(x) for x in input]
    # input = utils.split_list(input, "")
    # input = [x for x in input]
    # input = [int(x) for x in input[0].split(',')]
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    input = [[int(s) for s in x] for x in input] # Parse a 2-d number grid



def part1():
    
    visible_map = utils.make2dArray(len(input[0]), len(input), 0)
    
    
    for y, row in enumerate(input):
        row_max = -1
        for x, val in enumerate(row):
            # print(x, y, val)

            if val > row_max:
                # print("tall", x, y, val, row_max)
                row_max = val
                visible_map[y][x] = 1

        row_max = -1
        for x, val in reversed(list(enumerate(row))):
            # print(x, y, val)
            if val > row_max:
                # print("tall", x, y, val, row_max)
                row_max = val
                visible_map[y][x] = 1
            
    
    # print("Vertical -- \n")
    
    for x in range(len(input[0])):
        col_max = -1
        for y in range(len(input)):
            val = input[y][x]
            # print(x, y, val)
            
            if val > col_max:
                # print("tall3", x, y, val, col_max)
                
                col_max = val
                visible_map[y][x] = 1
                
        col_max = -1
        for y in range(len(input)-1, -1, -1):
            val = input[y][x]
            # print(x, y, val, col_max)
            
            if val > col_max:
                # print("tall4", x, y, val, col_max)
                col_max = val
                visible_map[y][x] = 1
            
    #
    # print(input)
    # utils.printMatrix(visible_map)
    
    
    return sum([sum(row) for row in visible_map])
    
    
def part2():
    max_score = 0
    
    for y, row in enumerate(input[1:-1]):
        for x, val in enumerate(row[1:-1]):
            true_x = x+1
            true_y = y+1

            left = 0
            right = 0
            up = 0
            down = 0
            # print("\n: Finding score for tree at ", true_x, true_y, "Score: ", val)

            
            # print("left")
            for l in range(true_x-1, -1, -1):
                # print("Checking ", true_y, l, "score: ", input[true_y][l])
                left = left + 1
                if input[true_y][l] >= val:
                    # print("blocked left at")
                    # print(input[true_y][l], l, left)
                    break
            
            # print("right")
            for r in range(true_x+1, len(row)):
                # print("Checking ", true_y, r, "score: ", input[true_y][r])
                right = right + 1
                if input[true_y][r] >= val:
                    # print("blocked right")
                    # print(input[true_y][r], r, right)
                    break
                    
            # print('up')
            for u in range(true_y-1, -1, -1):
                # print("Checking ", true_x, u, "score: ", input[u][true_x])
                up = up + 1
                if input[u][true_x] >= val:
                    # print("blocked up at")
                    # print(input[u][true_x], u, up)
                    break
                    
            # print('down')
            for d in range(true_y+1, len(input)):
                # print("Checking ", true_x, d, "score: ", input[d][true_x])
                down = down + 1
                if input[d][true_x] >= val:
                    # print("blocked down at")
                    # print(input[d][true_x], d, down)
                    break
                
            
            
            score = left * right * up * down
            # print("Score: ", score)
            
            if score >= max_score:
                max_score = score
            # Lef            
    
    
    return max_score


# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")