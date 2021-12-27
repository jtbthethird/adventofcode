import utils
import time
import copy
import re
import heapq
import numpy as np
import os
from os import path

day = 15

filename="input"+str(day)+".txt"
# filename="testinput"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    input = [l.strip() for l in f.readlines()] # One entry for each line
    
    # input = [x for x in input]
    # input = [int(x) for x in input[0].split(',')]
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    input = [[int(s) for s in x] for x in input]
        

# came_from is a map from a node to the previous node
def reconstruct_path(came_from, current):
    # total_path := {current}
    # while current in cameFrom.Keys:
        # current := cameFrom[current]
        # total_path.prepend(current)
    # return total_path
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.insert(0, current)
    return total_path

def est_distance(n, goal):
    x_dist = goal[0] - n[0]
    y_dist = goal[1] - n[1]
    return (x_dist + y_dist)

def get_neighbors(n, m):
    x = n[0]
    y = n[1]
    neighbors = []
    if x > 0:
        neighbors.append((x-1, y, m[y][x-1]))
    if x < len(m[0]) - 1:
        neighbors.append((x+1, y, m[y][x+1]))
    if y > 0:
        neighbors.append((x, y-1, m[y-1][x]))
    if y < len(m) - 1:
        neighbors.append((x, y+1, m[y+1][x]))
    return neighbors
    
    
def print_path(came_from, current, m):
    path = reconstruct_path(came_from, current)
    m1 = utils.make2dArray(len(m[0]), len(m), '.')
    for p in path:
        m1[p[1]][p[0]] = "█"
    # time.sleep(0.1)
    os.system("clear")
    utils.printMatrix(m1)

def a_star(start, goal, h, m, show=True):
    # The set of discovered nodes that may need to be (re-)expanded.
    # Initially, only the start node is known.
    # This is usually implemented as a min-heap or priority queue rather than a hash-set.
    nodes_to_search = [(0, start)]
    
    came_from = {}
    
    # Score from start to n
    gscore = {}
    gscore[start] = 0
    
    # fScore = estimate of total distance through n
    fscore = {}
    fscore[start] = h(start, goal)
    
    count = 0
    
    while nodes_to_search:
        count += 1
        # sorted(nodes_to_search, key=lambda x: fscore[x])
        # print(nodes_to_search)
        current = heapq.heappop(nodes_to_search)[1]

        # print("Current: ", current)
        if count % 10000 == 0:
            print("%d Current: "%count, gscore[current], current, len(nodes_to_search))
        
        if show:
            print_path(came_from, current, m)
        #
        if current == goal:
            print_path(came_from, current, m)
            return reconstruct_path(came_from, current)
        
        
        neighbors = get_neighbors(current, m)
    
        for neighbor in neighbors:
            tentative_g_score = gscore[current] + neighbor[2]
            if neighbor not in gscore:
                gscore[neighbor] = 1000000000000000000000 # really big number
            if tentative_g_score < gscore[neighbor]:
                # // This path to neighbor is better than any previous one. Record it!
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + h(neighbor, goal)
                
                if neighbor not in nodes_to_search:
                    heapq.heappush(nodes_to_search, (fscore[neighbor], neighbor))
                    # nodes_to_search.append(neighbor)
        
    return None
    

def part1():
    # print(input)
    #
    # print("Test")
    # print(len(input))
    # os.system("clear")
    # print("Test 2")
    start = (0, 0, 0)
    end = (len(input[0])-1, len(input)-1, input[-1][-1])
    
    # print(start, end)
    
    path = a_star(start, end, est_distance, input, show=False)

    # print(path)
    
    return sum([x[2] for x in path])
    

def part2():
    # print(len(input), len(input[0]))
        
    big_out = []
    for i in range(5):
        m_base = [[v+i if v+i < 10 else (v+i-9) for v in row] for row in input]

        big_row = copy.deepcopy(m_base)
        # print(i)
        # utils.printMatrix(m_base)
        for j in range(1, 5):
            # print(i, j)
            m2 = [[v+j if v+j < 10 else (v+j-9) for v in row] for row in m_base]
            
            raw = [v for row in m2 for v in row]
            # print("avg: ", sum(raw)/len(raw))
            
            for y, row in enumerate(m2):
                # print(y, row)
                big_row[y] += row
            # utils.printMatrix(big_row)
        
        # print("After %d rows"%i)
        big_out += copy.deepcopy(big_row)
        
    # utils.printMatrix(big_out)
    
    start = (0, 0, 0)
    end = (len(big_out[0])-1, len(big_out)-1, big_out[-1][-1])
        
    path = a_star(start, end, est_distance, big_out, show=False)

    return sum([x[2] for x in path])

# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")