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

day = "17"

filename="input_"+str(day)+".txt"
# filename="test_"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    input = [l.strip() for l in f.readlines()] # One entry for each line
    input = [c for c in input[0]]
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


rocks=[[['#', '#', '#', '#']], [['.', '#', '.'], ['#', '#', '#'], ['.', '#', '.']], [['.', '.', '#'], ['.', '.', '#'], ['#', '#', '#']], [['#'], ['#'], ['#'], ['#']], [['#', '#'], ['#', '#']]]


def print_falling_rock(rock, rock_pos, rock_map):
    rock_map2 = copy.deepcopy(rock_map)
    for y, row in enumerate(rock):
        for x, val in enumerate(row):
            if val == '#':
                rock_map2[y + rock_pos[1]][x + rock_pos[0]] = '@'
                
    utils.printMatrix(rock_map2)

def can_move_left(rock, rock_pos, rock_map):
    if rock_pos[0] == 0:
        return False
        
    for y, row in enumerate(rock):
        for x, val in enumerate(row):
            spot_left = rock_map[rock_pos[1] + y][rock_pos[0] + x - 1]
            if val == '#' and spot_left == '#':
                return False
        
    return True


def can_move_right(rock, rock_pos, rock_map):
    if rock_pos[0] + len(rock[0]) == len(rock_map[0]):
        return False
        
    for y, row in enumerate(rock):
        for x, val in enumerate(row):
            spot_right = rock_map[rock_pos[1] + y][rock_pos[0] + x + 1]
            if val == '#' and spot_right == '#':
                return False
    return True
    

def can_move_down(rock, rock_pos, rock_map):
    rock_height = len(rock)
    rock_width = len(rock[0])
    
    index_below = rock_pos[1] + rock_height
    
    if index_below == len(rock_map):
        return False
        
    # below_rock = rock_map[index_below][rock_pos[0]:rock_pos[0]+rock_width]
    
    # if rock[0] == rocks[1][0]:
        # print("Rock: ")
        # utils.printMatrix(rock)
    
    # if all([x == '.' for x in below_rock]):
    #     print(below_rock)
    #     print("Empty row, feel free to move")
    #     return True
        
    for y, row in enumerate(rock):
        for x, val in enumerate(row):
            spot_down = rock_map[rock_pos[1] + y + 1][rock_pos[0] + x]
            if val == '#' and spot_down == '#':
                return False
    
    return True
    

def drop_rock(rock_index, windex, rock_map, animate=False, speed=0.1):
    rock = np.array(rocks[rock_index])
    
    rock_height = len(rock)
    
    
    # Ensure the rock starts at the right place
    empty_rows = 0
    for y in range(len(rock_map)):
        if rock_map[y] == ['.', '.', '.', '.', '.', '.', '.']:
            empty_rows = empty_rows + 1
        else:
            break
    
    expansion = rock_height
    if empty_rows > 3:
        expansion = rock_height - (empty_rows - 3)

    
    rock_pos = (2, 0)
    
    if expansion > 0:
        rock_map = utils.expand2dArray(rock_map, 0, 0, expansion, 0, '.')
    else:
        rock_pos = (2, -expansion)

    rock_is_stuck = False
    
    # print("Starting the rock drop")
    # print_falling_rock(rock, rock_pos, rock_map)
    # print()
    
    while not rock_is_stuck:
        # print("\n\n------ Step --------")
        # print("Rock position to start: ", rock_pos)
        wind = input[windex]
        windex = (windex + 1) % len(input)
        
        if animate:
            utils.clear_terminal()
            print_falling_rock(rock, rock_pos, rock_map)
            print("Next step. Push ", wind)
            print("Windex: ", windex)
            time.sleep(speed)
        
        
        # Push the rock
        if wind == '<' and can_move_left(rock, rock_pos, rock_map):
            # print("pushing left")
            rock_pos = (rock_pos[0] - 1, rock_pos[1])
        elif wind == '>' and can_move_right(rock, rock_pos, rock_map):
            # print("pushing right")
            rock_pos = (rock_pos[0] + 1, rock_pos[1])

        # print("Rock position after wind: ", rock_pos)
        
        if animate:
            utils.clear_terminal()
            print_falling_rock(rock, rock_pos, rock_map)
            print("Next step. Drop ")
            print("Windex: ", windex)
            time.sleep(speed)
        
        
        # Drop the rock
        if can_move_down(rock, rock_pos, rock_map):
            # print("Moving down")
            rock_pos = (rock_pos[0], rock_pos[1] + 1)
        else:
            # print("Stopping!", rock_pos)
            # utils.printMatrix(rock_map)
            for y, row in enumerate(rock):
                for x, val in enumerate(row):
                    if val == '#':
                        yy = rock_pos[1] + y
                        xx = rock_pos[0] + x
                        rock_map[yy][xx] = '#'
            return (windex, rock_map)
    
    
def get_tower_height(rock_map):
    tower_height = len(rock_map)
    
    empty_rows = 0
    for y in range(len(rock_map)):
        if rock_map[y] == ['.', '.', '.', '.', '.', '.', '.']:
            empty_rows = empty_rows + 1
        else:
            break
    
    return (tower_height - empty_rows)
    

def part1():
    width = 7
    initial_height = 3
    
    rock_map = utils.make2dArray(width, initial_height, '.')
    
    windex = 0
    rock_index = 0
    
    for i in range(2022):
        # print("\n\n------ Step --------")
        # print("Rock index: ", rock_index)
        (windex, rock_map) = drop_rock(rock_index, windex, rock_map, animate=False, speed=0.5)

        #
        # rock_index = rock_index + 1
        rock_index = (rock_index + 1) % len(rocks)
        
        # print_tower_height(rock_map)
        

    # print("After step: ")
    # utils.printMatrix(rock_map)
    
    tower_height = len(rock_map)
    
    empty_rows = 0
    for y in range(len(rock_map)):
        if rock_map[y] == ['.', '.', '.', '.', '.', '.', '.']:
            empty_rows = empty_rows + 1
        else:
            break
    
    # print(tower_height, empty_rows)
    return tower_height - empty_rows
    

def get_top_row_as_num(rock_map):
    as_nums = [['0' if v == '.' else '1' for v in row] for row in rock_map[:30]]
    single_stream = [str(int(''.join(x for x in row), 2)) for row in as_nums]
    # print(single_stream)
    
    return ''.join(single_stream)
    
    
    
def get_top_flat_row(rock_map):
    for y in range(len(rock_map)):
        if rock_map[y] == ['#', '#', '#', '#', '#', '#', '#']:
            return len(rock_map) - y
    
    return 0
    

def is_duplicate(rock_map):
    
    empty_rows = 0
    for y in range(len(rock_map)):
        if rock_map[y] == ['.', '.', '.', '.', '.', '.', '.']:
            empty_rows = empty_rows + 1
        else:
            break


    height = len(rock_map) - empty_rows
    
    if height % 2 == 1:
        return False
        
    for y in range(int(height/2)):
        if rock_map[y] != rock_map[int(height/2) + y]:
            return False
    
    return True


def part2():
    width = 7
    initial_height = 3
    
    rock_map = utils.make2dArray(width, initial_height, '.')
    
    windex = 0
    rock_index = 0

    rock_0_set = {}
    
    diff_list = []
    
    i = 0
    last_height = 0
    while True:
        (windex, rock_map) = drop_rock(rock_index, windex, rock_map, animate=False, speed=0.1)

        rock_index = (rock_index + 1) % len(rocks)
        
        new_height = get_tower_height(rock_map)
        
        diff = new_height - last_height
        
        diff_list.append(diff)
        
        # print# ("Rock fell")
        # print("Windex / rock / height ", windex, rock_index, diff, i)
        
        tup = (windex, rock_index, diff, get_top_row_as_num(rock_map))
        print("TUP: ", i, tup, new_height)
        
        if tup not in rock_0_set:
            rock_0_set[tup] = (i, new_height)
        else:
            print("FOUND")
            
            print(diff_list)
            
            (initial_spot, initial_height) = rock_0_set[tup]
            
            period = i - initial_spot
            
            print("initial spot: ", initial_spot)
            print("Period: ", period)
            
            print("Last neight: ", initial_height)
            print("Current height: ", new_height)
            
            height_diff = new_height - initial_height
            
            print("diff: ", height_diff, diff)
            
            print("Iterations until 1000000000000")
            
            big = 1000000000000
            
            # How many times will it repeat from "initial spot" to before "big"
            repeats = math.floor((big - initial_spot) / period)
            
            print("Repeats: ", repeats)
            
            added_heights = repeats * height_diff
            
            
            remainder = big - initial_spot - (repeats * period)
            
            print("Remainder: ", remainder)
            
            remainder_list = diff_list[initial_spot + 1:(initial_spot + remainder)]
            print("Len: ", len(remainder_list))
            
            blocks_dropped = initial_spot + (repeats * period) + len(remainder_list)
            print("Dropped blocks: ", blocks_dropped)
            print(remainder_list)
            
            height_from_remainder = sum(remainder_list)
            
            print("height to add: ", height_from_remainder)
            
            total = initial_height + added_heights + height_from_remainder
            
            print(total == 1514285714288)
            
            return total
        
        last_height = new_height
        # print("Rock index: ", rock_index)
        # print("Height: ", )

    #     if get_top_flat_row(rock_map) > last_top_row:
    #         print("\n\n")
    #         print("A NEW ROW IS FLAT")
    #         print("Flat row: ", get_top_flat_row(rock_map))
    #         print("Windex: ", windex)
    #         print("Rock index: ", rock_index)
    #         print("Height: ", get_tower_height(rock_map))
    #         last_top_row = get_top_flat_row(rock_map)
    #         # time.sleep(2)
    #
        i = i + 1
        
        
    
    #
    #
    as_nums = [['0' if v == '.' else '1' for v in row] for row in rock_map]
    single_stream = [int(''.join(x for x in row), 2) for row in as_nums]
    
    
    top = single_stream[-10:]
    print(top)
    
    print(top in single_stream)
    # # print(single_stream)
    #
    # out = np.fft.fft(single_stream)
    #
    # # DRAW
    #
    # print(out)
    #
    # freq = np.fft.fftfreq(len(single_stream))
    #
    #
    # x_reconstructed = np.fft.ifft(out)
    #
    # print()
    #
    # print(freq)
    #
    # plt.plot(single_stream, out, label='Original')
    # plt.plot(len(single_stream), x_reconstructed, label='Reconstructed')
    # plt.xlabel('Time (s)')
    # plt.ylabel('Amplitude')
    # plt.legend()
    # plt.show()
    #
    
    
    return 0
    
# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")