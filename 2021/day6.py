import utils
import copy
import re
import numpy as np
from os import path

day = 6

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
    

def run_step(fish):
    # f2 = fish.copy()
    f2 = []
    for idx, f in enumerate(fish):
        if f == 0:
            fish[idx] = 6
            f2.append(8)
        else:
            fish[idx] = f-1
    f3 = fish + f2
    return f3


def part1():
    fish = input.copy()
    # print(fish)
    for i in range(80):
        fish = run_step(fish)
        # print(fish)
    return len(fish)
            

lookup = {}
def calculate_descendents(age, days_remaining):
   # print("Calcing: ", age, days_remaining)
   if (age, days_remaining) in lookup:
       return lookup[(age, days_remaining)]
   if age >= days_remaining:
       return 1
   mine = calculate_descendents(7, days_remaining-age)
   kids = calculate_descendents(9, days_remaining-age)
   tot = mine + kids
   lookup[(age, days_remaining)] = tot
   return tot
    
def part2():
    fish = input.copy()
    # print(fish)
    num = 0
    for f in fish:
        # print("Calculating for fish: ", f)
        n = calculate_descendents(f, 256)
        num += n
    return num
    
    

# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")