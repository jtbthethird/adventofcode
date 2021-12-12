import utils
import copy
import re
import numpy as np
from os import path

day = 8

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
    

def part1():
    outs = [v for line in input for v in line.split("|")[1].split()]
    return sum([1 for v in outs if len(v) in [2, 3, 4, 7]])
    

def add_arr_to_map(m, arr, num):
    m["".join(list(sorted(arr)))] = str(num)

def get_string_to_digit_map(signal):
    
    #    d
    # e    a
    #    f
    # g    b
    #    c
    
    #    7     5      5     5    3    6      6     4      6   2 
    # acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab
    #    8     5      2      3    7    9     6       4    0    1
    
    # Logic:
    # 1, 4, 7, 8
    # 3 (has all of the 7, one of the 4's, tells us what the bottom is, tells us what middle and top left are)
    # 2 (Of the two with 5, has the one that is also in the 3 (we just learned), and tells us the diff between the right two)
    # Should have them all now, just sort it out
    # 
    # Actually, use set logic. 
    # 

    s = [list(v) for v in sorted(signal, key=lambda x: len(x))]
    std_map = {}
    
    one = s[0]
    add_arr_to_map(std_map, one, 1)
    
    four = s[2]
    add_arr_to_map(std_map, four, 4)
    
    seven = s[1]
    add_arr_to_map(std_map, seven, 7)
    
    eight = s[-1]
    add_arr_to_map(std_map, eight, 8)

    s = [v for v in s if v not in [one, four, seven, eight]]
    
    three = [k for k in s if len(k) == 5 and set(seven).issubset(set(k))][0]
    add_arr_to_map(std_map, three, 3)
    s.remove(three)
    
    six = [k for k in s if len(k) == 6 and not set(one).issubset(set(k))][0]
    add_arr_to_map(std_map, six, 6)
    s.remove(six)
    
    five = [k for k in s if len(k) == 5 and set(k).issubset(set(six))][0]
    add_arr_to_map(std_map, five, 5)
    s.remove(five)
    
    two = [k for k in s if len(k) == 5 and k != three and k != five][0]
    add_arr_to_map(std_map, two, 2)
    s.remove(two)
    
    nine = [k for k in s if len(k) == 6 and set(five).issubset(set(k)) and k != six][0]
    add_arr_to_map(std_map, nine, 9)
    s.remove(nine)
    
    zero = s[0]
    add_arr_to_map(std_map, zero, 0)
    
    return std_map
    
    

    
def part2():  


    tally = 0
    for line in input:
        outs = ["".join(list(sorted(v))) for v in line.split("|")[1].split()]
        signal = line.split("|")[0].split()
        m = get_string_to_digit_map(signal)
        output = int("".join([m[k] for k in outs]))
        print(output)
        tally += output
    return tally
        
        
        
    

# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")