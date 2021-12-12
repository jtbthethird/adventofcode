import utils
import copy
import re
import numpy as np
from os import path

day = 3

filename="input"+str(day)+".txt"
# filename="testinput"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []
with open(filepath) as f:
    input = [l.strip() for l in f.readlines()] # One entry for each line
    
    # input = [x for x in input]
    
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    input = [[int(s) for s in x] for x in input]
 
# --- #
def part1():
    # print(len(input[0]))
    one_counts = np.sum(input, axis=0)
    # print(one_counts)
    gamma_array = []
    epsilon_array = []
    for c in one_counts:
        if c > len(input)/2:
            gamma_array.append(1)
            epsilon_array.append(0)
        else:
            gamma_array.append(0)
            epsilon_array.append(1)
            
    g_str = "".join([str(s) for s in gamma_array])
    e_str = "".join([str(s) for s in epsilon_array])

    g = int(g_str, 2)
    e = int(e_str, 2)
    return g*e
    # for i in input:
    # for x in range(len(counter)):
        # print(x))
    
    
    # print(c3)
        
    
def part2():
    remaining_values = np.array(input)
    
    o2_score = 0
    co2_score = 0

    for bit in range(len(input[0])):
        one_counts = np.sum(remaining_values, axis=0)
        # print(bit, one_counts[bit], len(remaining_values))
        val_at_bit = 0
        if one_counts[bit] >= len(remaining_values)/2:
            val_at_bit = 1
        
        # print("val_at_bit", val_at_bit)
        
        filt = [x[bit] == val_at_bit for x in remaining_values]
        # print("filter", filt)
        remaining_values = remaining_values[filt]
        # print(remaining_values)
        if (len(remaining_values) == 1):
            # print(remaining_values)
            o2_score = int("".join([str(s) for s in remaining_values[0]]), 2)
            break
            

    remaining_values = np.array(input)

    for bit in range(len(input[0])):
        one_counts = np.sum(remaining_values, axis=0)
        # print(remaining_values)
        # print(bit, one_counts[bit], len(remaining_values))
        val_at_bit = 0
        if one_counts[bit] < len(remaining_values)/2:
            val_at_bit = 1
        
        # print("val_at_bit", val_at_bit)
        
        filt = [x[bit] == val_at_bit for x in remaining_values]
        # print("filter", filt)
        remaining_values = remaining_values[filt]

        if (len(remaining_values) == 1):
            # print(remaining_values)
            co2_score = int("".join([str(s) for s in remaining_values[0]]), 2)
            break
    
    # print(o2_score, co2_score)
    
    return o2_score * co2_score
    

# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")