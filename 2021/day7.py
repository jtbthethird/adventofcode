import utils
import copy
import re
import numpy as np
from os import path

day = 7

filename="input"+str(day)+".txt"
# filename="testinput"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    input = [l.strip() for l in f.readlines()] # One entry for each line
    
    # input = [x for x in input]
    input = [int(x) for x in input[0].split(',')]
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[int(s) for s in x] for x in input]
    

def part1():
    print(input)
    l = min(input)
    r = max(input)
    
    min_pos = -1
    min_score = 1000000000000000000000
    for v in range(l, r+1):
        # print("checking pos: ", v)
        score = 0
        for c in input:
            dist = abs(c - v)
            score += dist
            # print("Dist for %d is %d"%(c, dist))
        # print("Total dist is: ", score)
        if score < min_score:
            min_pos = v
            min_score = score
    return min_score
            
    
def part2():
    print(input)
    l = min(input)
    r = max(input)
    
    memo = {}
    
    min_pos = -1
    min_score = 1000000000000000000000
    for v in range(l, r+1):
        # print("-----\nchecking pos: ", v)
        score = 0
        for c in input:
            dist = abs(c - v)
            d2 = 0
            if dist in memo:
                d2 = memo[dist]
            else:
                d2 = sum([i for i in range(dist+1)])
                memo[dist] = d2
            score += d2
            # print("Dist for %d is %d"%(c, d2))
        # print("Total dist is: ", score)
        if score < min_score:
            min_pos = v
            min_score = score
    return min_score
    

# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")