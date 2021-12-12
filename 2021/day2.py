import utils
import copy
import re
from os import path

day = 2

filename="input"+str(day)+".txt"
# filename="testinput"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []
with open(filepath) as f:
    input = [l.strip() for l in f.readlines()] # One entry for each line
    
    input = [x.split() for x in input]
    
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[s for s in x] for x in input]
 
def parseRow(row):
    if row[0] == "forward":
        return (int(row[1]), 0)
    if row[0] == "down":
        return (0, int(row[1]))
    if row[0] == "up":
        return (0, -int(row[1]))
 
# --- #
def part1():
    tally = [0, 0]
    for row in input:
        delta = parseRow(row)
        tally[0] += delta[0]
        tally[1] += delta[1]

    return tally[0] * tally[1]
        
    
def part2():
    pos = [0, 0]
    aim = 0
    for row in input:
        delta = parseRow(row)
        if (delta[1] != 0):
            aim += delta[1]
        if (delta[0] != 0):
            pos[0] += delta[0]
            pos[1] += aim * delta[0]


    return pos[0] * pos[1]
    

# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")