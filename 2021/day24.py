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

day = 24

filename="input"+str(day)+".txt"
# filename="testinput"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

inp = []

with open(filepath) as f:
    inp = [l.strip() for l in f.readlines()] # One entry for each line
    
    # input = [x for x in input]
    # input = [int(x) for x in input[0].split(',')]
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[int(s) for s in x] for x in input]

def get_b_int(b_str, vars):
    if b_str in ["w", "x", "y", "z"]:
        return vars[b_str]
    else:
        return int(b_str)
    
def get_input(prompt):
    return input(prompt)


def execute_line(line_str, vars, input_func, verbose=False):
    code = line_str.split(" ")[0]
    params = line_str.split(" ")[1:]
    if verbose:
        print(code, params)
    
    if code == "inp":
        # print(params[0])
        s = input_func("Enter your value: ")
        if verbose:
            print("input: ", s)
        # print(s)
        vars[params[0]] = int(s)
    elif code == "add":
        vars[params[0]] = vars[params[0]] + get_b_int(params[1], vars)
    elif code == "mul":
        vars[params[0]] = vars[params[0]] * get_b_int(params[1], vars)
    elif code == "div":
        b = get_b_int(params[1], vars)
        if b == 0:
            return -1
        vars[params[0]] = vars[params[0]] // b
    elif code == "mod":
        vars[params[0]] = vars[params[0]] % get_b_int(params[1], vars)
    elif code == "eql":
        if vars[params[0]] == get_b_int(params[1], vars):
            vars[params[0]] = 1
        else:
            vars[params[0]] = 0
    print("vars: ", vars)
    return 0
    
def monad_input(digits, current_index=0):
    def out(prompt):
        nonlocal current_index
        result = digits[current_index]
        current_index = current_index + 1
        # print("returning ", result)
        return result
    
    return out
    

def test_number(digits, verbose=False):
    if verbose:
        print("--- new test ---")
        print(digits)
    vars = {"w": 0, "x": 0, "y": 0, "z": 0}
    in_func = monad_input(digits)
    
    for line in inp:
        res = execute_line(line, vars, in_func, verbose)
        if res != 0:
            return False
    
    if verbose:
        print("Got ", vars["z"])
    return vars["z"] == 0    

def decrement_digits(digits):
    digits[-1] -= 1
    
    while 0 in digits:
        ind = digits.index(0)
        digits[ind] = 9
        digits[ind-1] -= 1
    
    return digits
    
def part1_try_2():
    # This is the one where we go digit by digit and restart the input if it looks off
    vars = {"w": 0, "x": 0, "y": 0, "z": 0}
    
    
    

def part1():
    # print(inp)
    
    # try_1 = 99999999999999 - 3040489030
    # print(try_1)

    # digits = [int(d) for d in list(str(try_1))]
    digits = [9]*14
    
    found_num = test_number(digits)
    
    while not found_num:
    # for i in range(11):
        digits = decrement_digits(digits)
        found_num = test_number(digits, True)
    
    return digits
    
    
def part2():
    return 0

# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")