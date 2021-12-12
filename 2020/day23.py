import template
import copy
import regex as re
import math 
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


filename="input23.txt"
# filename="testinput23.txt"

input = []
with open(filename) as f:
    input = [[int(x) for x in groups.split('\n')[1:]] for groups in f.read().split('\n\n')]
    # input = f.readlines()
    # input = [int(x.strip()) for x in input[0].split(',')]
    # input = [[z for z in x.strip()] for x in input]
    # input = [x.strip() for x in input]
    
input = '598162734'
# input = '389125467' # Test input

# --- #

def do_move(cups):
    current_cup = cups[0]
    next_cups = cups[1:4]
    new_circle = np.concatenate((cups[:1], cups[4:]))
    
    dest_cup = current_cup - 1
    while dest_cup not in new_circle:
        dest_cup = dest_cup - 1
        if dest_cup <= 0:
            dest_cup = max(new_circle)
    
    dest_index = np.where(new_circle == dest_cup)[0][0]
    
    dest_circle = np.concatenate((new_circle[0:dest_index+1], next_cups, new_circle[dest_index+1:]))
    
    return dest_circle
    

def part1():
    cups = np.array([int(v) for v in input])
    # print(cups)
    
    moves = 100
    for i in range(moves):
        # print("Doing a move: ")
        # print("Before: ", cups)
        cups = do_move(cups)
        # print("After: ", cups)
        cups = np.roll(cups, -1)

    while cups[0] != 1:
        cups = np.roll(cups, -1)
        
    return ''.join([str(v) for v in cups[1:]])
    


def do_move_linked(current_cup):
    # Point current cup to "next_cup 4"
    # current_cup's "one_less" points to "next_cup 1"
    # "next_cup 3" points to the one after "one_less"
    
    next_1 = current_cup.next_cup
    next_2 = next_1.next_cup
    next_3 = next_2.next_cup
    next_4 = next_3.next_cup
    
    next_ids = [next_1.id, next_2.id, next_3.id]
    
    one_less = current_cup.one_less
    while one_less.id in next_ids:
        one_less = one_less.one_less
    after_one_less = one_less.next_cup
    
    current_cup.next_cup = next_4
    one_less.next_cup = next_1
    next_3.next_cup = after_one_less
    
    return next_4
    
    
class Cup:
    def __init__(self, id, one_less):
        self.id = id
        self.one_less = one_less
        self.next_cup = None
        
def part2b():
    max_cup = 1000000
    moves = 10000000
    
    def print_cups(first_cup, n):
        cup = first_cup
        l = []
        while len(l) < n:
            l.append(cup.id)
            cup = cup.next_cup
        print(', '.join([str(v) for v in l]))
    
    cup_ids = np.array([int(v) for v in input])
    starter_cups = {}
    last_cup = None
    for cid in cup_ids:
        cup = Cup(cid, None)
        starter_cups[cid] = cup
        if last_cup is not None:
            last_cup.next_cup = cup
        last_cup = cup
    
    for i in range(0, 9):
        cup = starter_cups[cup_ids[i]]
        if cup.id > 1:
            cup.one_less = starter_cups[cup.id - 1]

    
    current_cup = starter_cups[cup_ids[0]]
    one_cup = starter_cups[1]
    
    cup_one_less = starter_cups[9]
    prev_cup = starter_cups[cup_ids[-1]]
    for i in range(10, max_cup+1):
        c = Cup(i, cup_one_less)
        prev_cup.next_cup = c
        prev_cup = c
        cup_one_less = c
    one_cup.one_less = cup_one_less
    prev_cup.next_cup = current_cup
    
    # DO THE WORK
    for i in range(moves):
        current_cup = do_move_linked(current_cup)
    
    two_cups_after_one = [one_cup.next_cup.id, one_cup.next_cup.next_cup.id]
    
    print(two_cups_after_one)
    
    return two_cups_after_one[0] * two_cups_after_one[1]
    
    
    
def part2():
    cups = np.array([int(v) for v in input])
    print(cups)
    
    cups = np.concatenate((cups, np.arange(10, 1000)))
    print(cups)
    
    moves = 10000
    for i in range(moves):
        # if i % 10000 == 0:
        print("Start of Round %d"%i)
        ind = np.where(cups == 1)[0][0]
        print(cups[ind+1:ind+3])
        # print("Doing a move: ")
        # print("Before: ", cups)
        cups = do_move(cups)
        print("After: ", np.roll(cups, i))
        cups = np.roll(cups, -1)
        # print("After: ", cups)
        # print(cups)
    
    return 2

# --- #

if __name__ == "__main__":
    template.funWrapper(part1, "Part 1")
    template.funWrapper(part2b, "Part 2")

    
        