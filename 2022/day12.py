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

day = "12"

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
    
    number_map = [[1 if s == 'S' else 26 if s =='E' else ord(s) - 96 for s in x] for x in input] # Parse a 2-d number grid
    area = len(number_map) * len(number_map[0])




def printPath(path):
    i2 = [[c for c in r] for r in input]
    
    # utils.printMatrix(i2)
    
    for p in path:
        i2[p[1]][p[0]] = "█"
        
    utils.printMatrix(i2)

def get_next_nodes(current_node, path):
    (x, y) = current_node
    current_val = number_map[y][x]
    
    nodes = set()
    if y > 0:
        up_coords = (x, y - 1)
        up = number_map[y - 1][x]
        if up - current_val <= 1 and up_coords not in path:
            nodes.add(up_coords)
    if y < len(number_map) - 1:
        down_coords = (x, y + 1)
        down = number_map[y + 1][x]
        if down - current_val <= 1 and down_coords not in path:
            nodes.add(down_coords)
    if x > 0:
        left_coords = (x - 1, y)
        left = number_map[y][x - 1]
        if left - current_val <= 1 and left_coords not in path:
            nodes.add(left_coords)
    if x < len(number_map[0]) - 1:
        right_coords = (x + 1, y)
        right = number_map[y][x + 1]
        if right - current_val <= 1 and right_coords not in path:
            nodes.add(right_coords)
    
    return nodes


dead_ends = set()

# Return the shortest path from node to goal
def DFS(node, goal, path=[], best=None):
    if node == goal:
        
        print("\n\n\n--------- (score: %d)"%len(path))
        printPath(path)
        
        return len(path)
        
    
    if best is not None and len(path) >= best:
        print("too long now... ", best)
        return best
    
    next_nodes = list(get_next_nodes(node, path))
    
    print(next_nodes)
    
    next_nodes.sort(key=lambda x: abs(goal[0] - x[0]) + abs(goal[1] - x[1]) - number_map[x[1]][x[0]])
    
    print(next_nodes)
    
    for next_node in next_nodes:
        # if next_node in dead_ends:
            # print("skipping b/c it's a dead end", next_node)
            # continue
            
        next_path = copy.copy(path)
        next_path.append(node)
        
        utils.clear_terminal()
        print("\n\n -- path -- ")
        printPath(next_path)
        
        next_node_best = DFS(next_node, goal, next_path, best)
        
        if next_node_best is None:
            # next_node seems like a dead end.
            dead_ends.add(next_node)
            continue
            
        if best is None:
            best = next_node_best
        elif next_node_best < best:
            best = next_node_best
    
    return best
    # Otherwise, Test each node around us


def reconstruct_path(node, came_from):
    path = []
    
    next_node = node
    while next_node:
        path.append(next_node)
        if next_node not in came_from:
            break
        next_node = came_from[next_node]
    
    return path

def A_star(start, goal, debug=False):

    start_node = ((start[0], start[1]), 0, abs(goal[0] - start[0]) + abs(goal[1] - start[1]))
    
    to_visit = [start]
    came_from = {}
    
    g_scores = defaultdict(lambda: math.inf) # Score from start to here
    g_scores[start] = start_node[1]
    f_scores = defaultdict(lambda: math.inf) # Estimate of total score through this node
    f_scores[start] = start_node[2]
    
    while to_visit:
        to_visit.sort(key=lambda x: f_scores[x])
        node = to_visit.pop(0)
        

        path = reconstruct_path(node, came_from)
        
        if debug:
            utils.clear_terminal()
            print("\n\n")
            printPath(path)
        
        if node == goal:
            # Reconstruct the path
            path = reconstruct_path(node, came_from)
    
    
            print("\n\n")
            printPath(path)
            return len(path)-1
        
        next_nodes = get_next_nodes(node, [])
        
        
        for n in next_nodes:
            d = 1
            # if number_map[n[1]][n[0]] > number_map[node[1]][node[0]]:
#                 d = 0
#             elif number_map[n[1]][n[0]] < number_map[node[1]][node[0]]:
#                 d = 20
            g_temp = g_scores[node] + d
            if g_temp < g_scores[n]:
                came_from[n] = node
                g_scores[n] = g_temp
                f_scores[n] = g_temp + abs(goal[0] - n[0]) + abs(goal[1] - n[1]) + number_map[goal[1]][goal[0]] - number_map[n[1]][n[0]]
                if n not in to_visit:
                    to_visit.append(n)
    
    
    return 0
    
    

def part1():
    utils.printMatrix(input)
    
    start = (0, 0)
    for y, row in enumerate(input):
        for x, val in enumerate(row):
            if val == 'S':
                start = (x, y)
            elif val == 'E':
                end = (x, y)
                
    
    score = A_star(start, end)
    
    return score

    
    
def part2():
    
    valid_starts = set()
    
    for y, row in enumerate(input):
        for x, val in enumerate(row):
            if val == 'a':
                if x > 0 and row[x-1] == 'b':
                    valid_starts.add((x, y))
                    continue
                if y > 0 and input[y-1][x] == 'b':
                    valid_starts.add((x, y))
                    continue
                if x < len(row) - 1 and row[x+1] == 'b':
                    valid_starts.add((x,y))
                    continue
                if y < len(input) - 1 and input[y+1][x] == 'b':
                    valid_starts.add((x,y))
                    continue
    
    
    min_length = math.inf
    min_spot = None
    for y, row in enumerate(input):
        for x, val in enumerate(row):
            if val == 'S':
                start = (x, y)
            elif val == 'E':
                end = (x, y)
    
    for starter in valid_starts:
        dist = A_star(starter, end)
        
        if dist < min_length:
            min_length = dist
            min_spot = starter
    
                
    
    return min_length
    
# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")