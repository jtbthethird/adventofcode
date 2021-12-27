import utils
import time
import copy
import math
import re
import heapq
import numpy as np
import os
from collections import Counter
from os import path

day = 23

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
    # input = [[int(s) for s in x] for x in input]

energy_needs = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000
}

destination_x = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}


def print_grid(grid):
    utils.printMatrix(np.pad(np.array(grid), 1, "constant", constant_values="#"))
    
def hole_is_empty(grid, column):
    hole_contents = np.array(grid)[:,column]
    hole_contents_bool = [v == "." for v in hole_contents]

    return np.all(hole_contents_bool)

class Amphipod:
    def __init__(self, atype, starting_spot, id, is_part_2=False):
        self.type = atype
        self.position = starting_spot
        self.id = id
        self.in_hallway = False
        self.cost = energy_needs[self.type]
        self.is_part_2 = is_part_2
    
    # def 
    def is_done(self, grid):
        if self.position[0] != destination_x[self.type]:
            return False
        
        g = np.array(grid)
        
        me_down = g[self.position[1]:,self.position[0]]
        # print("is done", me_down, self.type, self.position, np.all([v == self.type for v in me_down]))
        return np.all([v == self.type for v in me_down])
    
    # def is_done_old(self, grid):
    #     if self.position[0] != destination_x[self.type]:
    #         return False
    #
    #     if self.is_part_2:
    #         return self.is_done_2(grid)
    #
    #     # print(self.position)
    #     if self.position[1] == 2:
    #         return True
    #
    #     # print(grid)
    #     below = grid[self.position[1]+1][self.position[0]]
    #     if below == self.type or below == ".":
    #         return True
    #
    #     return False
        
    def can_go_home(self, grid):
        if self.is_in_hole() and not self.can_leave_hole(grid):
            return False
        # The target hole must either be empty or only have a companion
        target_hole = destination_x[self.type]
        if hole_is_empty(grid, target_hole):
            return True
        
        hole_contents = [v for row in grid for x,v in enumerate(row) if x == target_hole]
        # print(hole_contents)
        
        return np.all([x == "." or x == self.type for x in hole_contents])
    
    def is_in_hole(self):
        return self.position[1] > 0
    
    def can_leave_hole(self, grid):
        return self.position[1] > 0 and grid[self.position[1]-1][self.position[0]] == "."
        # return self.position[1] == 1 or grid[1][self.position[0]] == "."
        
    def can_reach_position(self, x, y, grid):
        if self.is_in_hole():
            if not self.can_leave_hole(grid):
                return False
        else:
            if not self.can_go_home(grid):
                return False
        hallway_path = grid[0][min(self.position[0],x)+1:max(self.position[0],x)]
        
        return np.all([x == "." for x in hallway_path])
            
    
    def get_available_moves(self, grid):
        """ Return a list of moves. A move is (targetx, targety, cost, type, fromx, fromy, pod)"""
        if self.is_done(grid):
            return []
        if self.can_go_home(grid):
            # print("%s can go home from %d,%d"%(self.type, self.position[0], self.position[1]))
            target_col = destination_x[self.type]
            
            # Get the lowest open hole
            target_y = max([y for y,row in enumerate(grid) if row[target_col] == "."])

            # Check that the path is clear
            if self.can_reach_position(target_col, target_y, grid):
                distance = abs(target_col - self.position[0]) + target_y + self.position[1]

                return [(target_col, target_y, distance * self.cost, self.type, self.position[0], self.position[1], self)]
        
        if self.is_in_hole():
            # We're in the hole, need to find a space on the outside
            if not self.can_leave_hole(grid):
                # We're blocked, so never mind
                return []
            options = []
            for x,i in enumerate(grid[0]):
                if x in destination_x.values():
                    continue
                if i == ".":
                    if self.can_reach_position(x,0,grid):
                        # out_cost = (abs(x - self.position[0]) + self.position[1])*self.cost
                        # in_cost = (abs(x - destination_x[self.type]) + 2) * self.cost
                        options.append((x,0,(abs(x - self.position[0]) + self.position[1])*self.cost, self.type, self.position[0], self.position[1], self))
            
            options = sorted(options, key=lambda move: move[2])
            
            return options
        else:
            # We're not in the hole and can't go home, soooo. I guess we're done here.
            return []
    
def get_memo_key(grid, pods, operations):
    score = sum([s[2] for s in operations])
    grid_str = "".join([v for row in grid for v in row])
    return grid_str + " - " + str(score)

def find_best_operations(pods, grid, best=-1, operations=[], memo={}):
    # print(operations)
    # print_grid(grid)

    if np.all([p.is_done(grid) for p in pods]):
        total_cost = sum([s[2] for s in operations])
        print("Found a solution: ", total_cost)
        # print_grid(grid)
        return total_cost
    
    
    key = get_memo_key(grid, pods, operations)
    if key in memo:
        # print("Got a memo: ", key)
        return memo[key]
    
    move_list = []
    
    for i,pod in enumerate(pods):
        next_moves = pod.get_available_moves(grid)
        # if next_moves:
        # print()
        # print("Checking moves")
        # print(operations)
        # print(i, pod.type, pod.position, next_moves)
        # print_grid(grid)
        
        for move in next_moves:
            if best > 0 and sum([s[2] for s in operations]) + move[2] > best:
                continue
                
            
                
            
            # Make the move
            # Do so by making a copy of all the shit
            next_pods = copy.copy(pods)
            next_pods[i] = copy.deepcopy(pod)
            new_pos = (move[0], move[1])
            next_pods[i].position = new_pos
            
            grid_copy = copy.deepcopy(grid)
            grid_copy[new_pos[1]][new_pos[0]] = pod.type
            grid_copy[pod.position[1]][pod.position[0]] = "."
            
            op_copy = copy.deepcopy(operations)
            op_copy.append(move)
            
            # print("Moving %s to "%pod.type, new_pos)
            # print_grid(grid_copy)
            # print(op_copy)
            # print()
            
            res = find_best_operations(next_pods, grid_copy, best, op_copy)
            if res > 0:
                if best == -1:
                    best = res
                elif res < best:
                    # print("New best: ", res)
                    best = res
    memo[key] = best
    return best

def init(is_part_2=False):
    hallway = input[1][1:-1]
    # print(len(hallway), hallway)
    
    row0 = list(input[2].replace("#", ""))
    row1 = list(input[3].replace("#", ""))
    
    #
    #D#C#B#A#
    #D#B#A#C#
    #
    
    part_2_row1 = ["D","C","B","A"]
    part_2_row2 = ["D","B","A","C"]
    # part_2_row2 = ["A","B","C","D"] # Just for testing
    
    holes = [row0, row1]
    if is_part_2:
        holes = [row0, part_2_row1, part_2_row2, row1]
    
    height = 3
    if is_part_2:
        height=5
        
    grid = utils.make2dArray(len(hallway), height, ".")
    
    ys = [1,2]
    if is_part_2:
        ys = ys + [3,4]
    for y in ys:
        for x in range(len(hallway)):
            if x in destination_x.values():
                continue
            grid[y][x] = "#"
            
    pods = []
    
    i = 0
    for y, row in enumerate(holes):
        for x, val in enumerate(row):
            pod = Amphipod(val, (x*2 + 2, y+1), i)
            grid[y+1][x*2 + 2] = pod.type
            # print(pod.position, pod.type)
            pods.append(pod)
            i += 1
            
    return (pods, grid)

def part1():
    (pods, grid) = init()

    print("--- Starter ---")
    print_grid(grid)
    
    pods[0].can_go_home(grid)
    
    result = 15338
    result = find_best_operations(pods, grid)
    
    test_result = 12521
    
    return result
    
    
def part2():
    (pods, grid) = init(True)

    print("--- Starter ---")
    print_grid(grid)
    
    pods[0].can_go_home(grid)
    
    result = 15338
    result = find_best_operations(pods, grid)
    
    test_result = 44169
    
    return result


# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")