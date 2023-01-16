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

day = "15"

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
    pairs = []
    for row in input:
        m = re.match(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)", row)
        pair = [int(g) for g in m.groups()]
        # print(pair)
        dist = abs(pair[0] - pair[2]) + abs(pair[1] - pair[3])
        pairs.append(((pair[0], pair[1]), (pair[2], pair[3]), dist))
        


def get_covered_ranges_for_y(y):
    min_x = min(p[1][0] for p in pairs)
    max_x = max(p[1][0] for p in pairs)
    
    # print("x range: ", min_x, max_x))
    
    # THen go through item by item on row Y (10 for test, 2000000 for prod)
    count = 0

    # For each sensor, calculate its range on row y
    covered = []
    
    for p in pairs:
        (sensor, beacon, dist) = p
        # print("sensor, distance", sensor, dist)
        dist_to_y = abs(y - sensor[1])
        remaining = dist - dist_to_y
        # print("distance to y | remaining from sensor", dist_to_y, remaining)
        
        if remaining >= 0:

            low_x = sensor[0] - remaining
            high_x = sensor[0] + remaining
            # print(low_x, high_x)
            covered.append((low_x, high_x))


    # print(covered)
    
    c2 = copy.deepcopy(covered)

    combined_list = []
    
    # print("\n\n")
    # Take the first segment and match it against all the others
    #   If it has any overlap with another segment, combine the two into a new segment.
    #.  Then take that new segment and run it against all the other segments again. 
    #.  If you run through the whole list and have no matches, add it to a new "output" list
    #.  Repeat until the original list is empty
    while covered:
        segment = covered.pop(0)
        # print()
        # print("Matching: ", segment)
        
        changed = True
        while changed:
            changed = False
            # print("Matching (2): ", segment, covered)
            
            for i, other_seg in enumerate(covered):
                # print(i, other_seg)
                if (segment[0] >= other_seg[0] and segment[0] <= other_seg[1]) or \
                    (segment[1] >= other_seg[0] and segment[1] <= other_seg[1]) or \
                    (segment[0] <= other_seg[0] and segment[1] >= other_seg[1]) or \
                    (segment[0] == other_seg[1] + 1) or \
                    (segment[1] == other_seg[0] - 1):
                    
                    new_seg = (min(segment[0], other_seg[0]), max(segment[1], other_seg[1]))
                    # print("overlap: ", segment, other_seg, new_seg)
                    covered.pop(i)
                    changed = True
                    segment = new_seg
                    break
        
        combined_list.append(segment)
        
    # combined_list.sort(key=lambda x: x[0])

    
    return combined_list
    

def part1():    
    y = 10
    y = 2000000
    
    final_list = get_covered_ranges_for_y(y)

    beacons = list(set([p[1] for p in pairs]))

    
    return sum([x[1] - x[0] for x in final_list]) + 1 - sum([1 if b[1] == y else 0 for b in beacons])
    
    
def part2():
    
    y_range = 20
    y_range = 4000000
    
    for y in range(y_range + 1):
        l = get_covered_ranges_for_y(y)
        # print(y, l)
        if len(l) > 1:
            print(y, l)
            l.sort(key=lambda x: x[0])
            
            x = l[1][0] - 1
            return x * 4000000 + y
    
    
    return 1
    
# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")