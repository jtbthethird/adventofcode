import utils
import copy
import re
import numpy as np
from os import path

day = 13

# filename="input"+str(day)+".txt"
filename="testinput"+str(day)+".txt"

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

def print_paper(dots):
    
    max_x = max([d[0] for d in dots])
    max_y = max([d[1] for d in dots])
    
    m = utils.make2dArray(max_x+1, max_y+1, ".")
    
    for d in dots:
        m[d[1]][d[0]] = "#"
    
    utils.printMatrix(m)

def get_paper():
    dots = [[int(s) for s in line.split(",")] for line in input[:input.index("")]]

    folds = [(line.split("=")[0][-1], int(line.split("=")[1])) for line in input[input.index("")+1:]]

    
    return (dots, folds)

def do_fold(dots, axis):
    fold_d = axis[1]
    for d in dots:
        if axis[0] == "x" and d[0] >= fold_d:
            dist = d[0] - fold_d
            d[0] = fold_d - dist
        elif axis[0] == "y" and d[1] >= fold_d:
            dist = d[1] - fold_d
            d[1] = fold_d - dist
    
    # print("after: ", in_dots)
    # print_paper(in_dots)

def part1():
    (dots, folds) = get_paper()
    
    # print_paper(dots)
    
    do_fold(dots, folds[0])
    
    s = set([(d[0], d[1]) for d in dots])
    return len(s)
    

def part2():
    (dots, folds) = get_paper()
    
    # print_paper(dots)
    
    for fold in folds:
        do_fold(dots, fold)
    
    
    print_paper(dots)

# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")