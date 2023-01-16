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

day = "14"

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
    lines = []
    
    for row in input:
        points = [x.strip() for x in row.split('->')]
        for i in range(len(points) - 1):
            [x1, y1] = [int(v) for v in points[i].split(',')]
            [x2, y2] = [int(v) for v in points[i+1].split(',')]
            
            line_data = {}
            line_data['min_x'] = min(x1, x2)
            line_data['max_x'] = max(x1, x2)
            line_data['min_y'] = min(y1, y2)
            line_data['max_y'] = max(y1, y2)
            lines.append(line_data)

    min_y = min([x["min_y"] for x in lines])
    max_y = max([x["max_y"] for x in lines])
    min_x = min([x["min_x"] for x in lines])
    max_x = max([x["max_x"] for x in lines])
                
source = (500 - min_x + 1, 0)
        
print("Bounds: ", (min_x, max_x), max_y)



def get_sandmap():
    sand_map = utils.make2dArray(max_x - min_x + 3, max_y+2, '.')
    for line in lines:
        for x in range(line["min_x"], line["max_x"]+1):
            for y in range(line["min_y"], line["max_y"]+1):
                sand_map[y][x - min_x + 1] = "#"
                
    sand_map[0][source[0]] = '+'
    # utils.printMatrix(sand_map)
    
    return sand_map
    


# Return the grain's final resting point
def drop_sand(sand_map, part1=True):
    
    grain = source
    
    while grain[1] <= max_y:
        # print(grain)
        
        # If the spot 1 below is free, go there
        if sand_map[grain[1]+1][grain[0]] == '.':
            # print("Free")
            grain = (grain[0], grain[1] + 1)
            continue
        
        # Else if the spot one to the left is free, go there
        elif sand_map[grain[1] + 1][grain[0] - 1] == '.':
            # print("Free")
            grain = (grain[0] - 1, grain[1] + 1)
            continue
            
        
        # Else if the spot one to the right is free, go there
        elif sand_map[grain[1] + 1][grain[0] + 1] == '.':
            # print("Free")
            grain = (grain[0] + 1, grain[1] + 1)
            continue
        
        # Else, rest.
        else:
            # print("Fail", grain)
            return grain
            
    if part1:
        return -1
    else:
        return grain


def part1():
    # print(lines)
    
    count = 0
    sandmap = get_sandmap()
    
    while True:
        result = drop_sand(sandmap)
        
        if result == -1:
            utils.printMatrix(sandmap)
            return count
    
        count += 1
        sandmap[result[1]][result[0]] = '█'

    return 1
    
    
def part2():
    global source
    
    count = 0
    sandmap = get_sandmap()
    
    while True:
        result = drop_sand(sandmap, part1=False)
        # print(result)
        
        if result[1] == 0:
            count = count + 1
            # print("Done!")
            sandmap[result[1]][result[0]] = '█'

            sandmap = utils.expand2dArray(sandmap, 0, 0, 0, 1, '#')
            utils.printMatrix(sandmap)
            return count
    
        
        count += 1
        sandmap[result[1]][result[0]] = '█'
        
        
        if result[0] == 0:
            # print("Move right!")
            sandmap = utils.expand2dArray(sandmap, 1, 0, 0, 0, '.')
            
            source = (source[0] + 1, source[1])
        
        if result[0] == len(sandmap[0])-1:
            # print("Move left!")
            sandmap = utils.expand2dArray(sandmap, 0, 1, 0, 0, '.')
            
        
        # utils.printMatrix(sandmap)
    
    return 1
    
# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")