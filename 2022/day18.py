import utils
import time
import string
import itertools
import copy
import math
import regex
import re
import heapq
import numpy as np
import os
from collections import Counter, defaultdict
from os import path
import functools
import operator
import json
import matplotlib.pyplot as plt

day = "18"

filename="input_"+str(day)+".txt"
# filename="test_"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    input = [l.strip() for l in f.readlines()] # One entry for each line
# filename="test_"+str(day)+".txt"
#     input = [c for c in input[0]]
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
    input = [tuple([int(v) for v in row.split(',')]) for row in input]


def get_all_touching_points(p):
    up =    (p[0], p[1] + 1, p[2])
    down =  (p[0], p[1] - 1, p[2])
    left =  (p[0] - 1, p[1], p[2])
    right = (p[0] + 1, p[1], p[2])
    front = (p[0], p[1], p[2] - 1)
    back =  (p[0], p[1], p[2] + 1)
    
    return [up, down, left, right, front, back]

def part1():
    # print(input)
    
    points = set()
    
    for point in input:
        # print(point)
        (x, y, z) = point
        points.add(point)
        
    open_faces = 0
    
    for point in points:
        touching = get_all_touching_points(point)
        for t in touching:
            if t not in points:
                open_faces = open_faces + 1
        
    return open_faces
    
    
def is_in_bounds(point, bounds):
    return point[0] >= bounds[0][0] and point[0] <= bounds[0][1] and point[1] >= bounds[1][0] and point[1] <= bounds[1][1] and point[2] >= bounds[2][0] and point[2] <= bounds[2][1]

    
def part2():
    points = set()
    
    for point in input:
        # print(point)
        (x, y, z) = point
        points.add(point)
        
    open_faces = 0
    
    for point in points:
        touching = get_all_touching_points(point)
        for t in touching:
            if t not in points:
                open_faces = open_faces + 1
    
    # print(points)
    
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    zs = [p[2] for p in points]
    

    # print(xs, ys, zs)
    
    x_range = (min(xs), max(xs))
    y_range = (min(ys), max(ys))
    z_range = (min(zs), max(zs))
    
    bounds = ((min(xs) - 1, max(xs) + 1), (min(ys) - 1, max(ys) + 1), (min(zs) - 1, max(zs) + 1))
    
    # print(x_range, y_range, z_range)
    
    ranges = {}
    
    for x in range(x_range[0], x_range[1] + 1):
        for y in range(y_range[0], y_range[1] + 1):
            # z points on this line
            line = [p[2] for p in points if p[0] == x and p[1] == y]
            if line:
                ranges[(x, y, 0)] = (min(line), max(line))
    
    
    
    for z in range(z_range[0], z_range[1] + 1):
        for y in range(y_range[0], y_range[1] + 1):
            # x points on this line
            line = [p[0] for p in points if p[2] == z and p[1] == y]
            if line:
                ranges[(0, y, z)] = (min(line), max(line))

    
    for x in range(x_range[0], x_range[1] + 1):
        for z in range(z_range[0], z_range[1] + 1):
            # y points on this line
            line = [p[1] for p in points if p[0] == x and p[2] == z]
            if line:
                ranges[(x, 0, z)] = (min(line), max(line))


    #
    
    
    # Do a BFS for all non-trapped gasses
    # Then every point that's "within the bounds" of the snowball but isn't a non-trapped gas and isn't snow is trapped. Do the same removal as before
    
    # BFS
    start_point = (x_range[0] - 1, y_range[0] - 1, z_range[0] - 1)
    
    points_to_check = set([start_point])
    untrapped_air = set()
    
    # Total range is one larger than the snowball range
    while points_to_check:
        point = points_to_check.pop()
        untrapped_air.add(point)
        
        adjascents = [p for p in get_all_touching_points(point)]
        
        for a in adjascents:
            if not is_in_bounds(a, bounds):
                continue
            if a in points_to_check or a in untrapped_air:
                continue
            if a in points:
                continue
            points_to_check.add(a)
        
    
    # print(len(untrapped_air))
        
        
    for x in range(x_range[0] + 1, x_range[1]):
        for y in range(y_range[0] + 1, y_range[1]):
            for z in range(z_range[0] + 1, z_range[1]):
                p = (x,y,z)
                if p in points or p in untrapped_air:
                    continue
                    
                # We're trapped
                # print("Trapped...", p)
                touching = get_all_touching_points((x, y, z))
                # print("Touching: ", touching)
                for t in touching:
                    if t in points:
                        # print("subtracting for ", t)
                        open_faces = open_faces - 1
    
        
    
    
    
    
    return open_faces
    
# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")