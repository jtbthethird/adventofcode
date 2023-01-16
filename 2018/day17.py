import utils
import time
import copy
import math
import re
import heapq
import numpy as np
import os
from collections import Counter, defaultdict
from os import path


day = "17"

filename="input_"+str(day)+".txt"
# filename="test_"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    # input = [x for x in f.readlines()[0]]
    input = [l.strip() for l in f.readlines()] # One entry for each line
    # input = [sorted([int(x) for x in y.split('x')]) for y in input]
    
    input = [[x.strip() for x in y.split(',')] for y in input]
    
    lines = []
    for line in input:
        line_data = {}
        fixed = int(line[0][2:])
        low_range = int(line[1][2:line[1].find('.')])
        high_range = int(line[1][line[1].rfind('.')+1:])
        # print(line, fixed, low_range, high_range)
        if line[0][0] == "x":
            line_data["min_x"] = fixed 
            line_data["max_x"] = fixed
            line_data["min_y"] = low_range
            line_data["max_y"] = high_range
        else:
            line_data["min_y"] = fixed
            line_data["max_y"] = fixed
            line_data["min_x"] = low_range
            line_data["max_x"] = high_range
        lines.append(line_data)
    # print(lines)
    
    min_y = min([x["min_y"] for x in lines])
    max_y = max([x["max_y"] for x in lines])
    min_x = min([x["min_x"] for x in lines])
    max_x = max([x["max_x"] for x in lines])
        
    print("Bounds: ", (min_x, max_x), max_y)

    # input = [x for x in input[0]]
    # input = ["" if x == '' else int(x) for x in input]
    # input = utils.split_list(input, "")
    # input = [x for x in input]
    # input = [int(x) for x in input[0].split(',')]
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[int(s) for s in x] for x in input]
    
    water_map = utils.make2dArray(max_x - min_x + 2, max_y+1, '.')
    for line in lines:
        for x in range(line["min_x"], line["max_x"]+1):
            for y in range(line["min_y"], line["max_y"]+1):
                water_map[y][x - min_x + 1] = "#"
    

def viz(fixed_water, pouring_water):
    arr = utils.make2dArray(max_x - min_x + 2, max_y+1, '.')
    
    for line in lines:
        for x in range(line["min_x"], line["max_x"]+1):
            for y in range(line["min_y"], line["max_y"]+1):
                arr[y][x - min_x + 1] = "#"
                
    for w in fixed_water:
        arr[w[1]][w[0] - min_x +1] = '~'
        
    for w in pouring_water:
        arr[w[1]][w[0] - min_x + 1] = "|"
    
    utils.printMatrix(arr)
    

def is_wall(point):
    return water_map[point[1]][point[0] - min_x + 1] == '#'
    
def is_water(point, water):
    return point in water
    
    
# return the number of water drops from here on out.
def do_drop(from_point, water):
    # Check the spot below. If it's open, return 1 + recurse
    # print("\ndropping at ", from_point)

    point_below = (from_point[0], from_point[1]+1)
    
    if point_below[1] > max_y:
        return 0
    
    if is_open(point_below, water):
        water.add(point_below)
        return 1 + do_drop(point_below, water)
    
    # print("We hit something at", from_point)
    return flood_row(from_point, water)
    


def flood_row(at_point, water):
    # print("flooding", at_point)
    point_left = (at_point[0]-1, at_point[1])
    point_right = (at_point[0]+1, at_point[1])
    
    spilled = False
    
    # Go left:
    left = 0
    while is_open(point_left, water):
        water.add(point_left)
        left = left + 1
        
        left_down = (point_left[0], point_left[1]+1)
        if is_open(left_down, water):
            left = left + do_drop(point_left, water)
            spilled = True
            break
        else:
            point_left = (point_left[0]-1, point_left[1])
    
    # print("Left", left)

    right = 0
    while is_open(point_right, water):
        water.add(point_right)
        right += 1
        
        right_down = (point_right[0], point_right[1]+1)
        if is_open(right_down, water):
            right += do_drop(point_right, water)
            spilled = True
            break
        else:
            point_right = (point_right[0]+1, point_right[1])
    # print("Right", right)
    
    # print(left+right, spilled)
    
    up = 0
    if not spilled:
        up = flood_row((at_point[0], at_point[1]-1), water)
    
    return left + right + up
    

def part1():
    # print(input)
    # print(max_y)
    
    # Initial idea...
    # Don't do a crazy array thing (unless the viz helps)
    # Instead, just keep a set of the completed squares, and a queue of squares that are falling
    # For the most recent falling one...
    #.   try to drop it down a step. ~~~Check for intersections~~~
    #.       If it can drop down, push the next square to the queue and go back to the start. 
    #.       Else, mark it as "stopped" and try to go sideways (both directions). Any new ones should be pushed to the stack.


    
    # Cases to handle
    # Falling drop (open below)
    # Hitting the bottom of a bucket (filling a row)
    # Moving up (hitting both sides of a bucket)
    # Overflowing (finding 1-2 overflow points, splitting in more streams)
    # Going past the bottom
    
    water = set()
    pouring_water = set()
    fixed_water = set()
    
    
    queue = [(500, 0)]
    
    while queue:
        at_point = queue.pop(0)
        # print("Dropping at", at_point)

        point_below = (at_point[0], at_point[1]+1)
    
        if point_below[1] > max_y:
            continue
    
        if not is_wall(point_below) and point_below not in water:
            water.add(point_below)
            pouring_water.add(point_below)
            queue.append(point_below)
            # return 1 + do_drop(point_below, water)
        elif point_below in pouring_water:
            continue
        elif is_wall(point_below) or point_below in fixed_water:
            # Flood row
            # print("flooding", at_point)
            point_left = (at_point[0]-1, at_point[1])
            point_right = (at_point[0]+1, at_point[1])
    
            spilled = False
    
            flood_points = set()
            # Go left:
            while not is_wall(point_left):
                # print("Adding water: ", point_left)
                flood_points.add(point_left)
        
                left_down = (point_left[0], point_left[1]+1)
                if not is_wall(left_down) and left_down not in fixed_water:
                    # print("Spilling left", point_left)
                    queue.append(point_left)
                    # left = left + do_drop(point_left, water)
                    spilled = True
                    break
                else:
                    point_left = (point_left[0]-1, point_left[1])
    
            while not is_wall(point_right):
                flood_points.add(point_right)
        
                right_down = (point_right[0], point_right[1]+1)
                if not is_wall(right_down) and right_down not in fixed_water:
                    # print("Spilling right", point_right)
                    queue.append(point_right)
                    spilled = True
                    break
                else:
                    point_right = (point_right[0]+1, point_right[1])
    

            water = water.union(flood_points)
            if not spilled:
                fixed_water = fixed_water.union(flood_points)
                fixed_water.add(at_point)
                pouring_water = pouring_water.difference(flood_points)
                if at_point in pouring_water:
                    pouring_water.remove(at_point)
                up = (at_point[0], at_point[1]-1)
                # print("Filled a bucket. Moving up to ", up)
                queue.append(up)
                pouring_water.add(up)
                water.add(up)
            else:
                pouring_water = pouring_water.union(flood_points)
                
    
            # return left + right + up
        # viz(fixed_water, pouring_water)
    
    
    # out =  do_drop((500, 0), water)
    
    viz(fixed_water, pouring_water)
    
    # print(water)

    print(len(water), len(fixed_water), len(pouring_water))
    
    return sum([1 for w in water if w[1] >= min_y])

    # return len(water)
    
def part2():
    
    return 0
    

# ---- #
    
if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")