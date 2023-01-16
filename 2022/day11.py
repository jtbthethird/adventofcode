import utils
import time
import string
import copy
import math
import re
import heapq
import numpy as np
import os
from collections import Counter, defaultdict
from os import path
import functools
import operator

day = "11"

filename="input_"+str(day)+".txt"
# filename="test_"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    input = [l.strip() for l in f.readlines()] # One entry for each line
    # input = [(x.split(' ')[0], int(x.split(' ')[1])) for x in input]
    # input = f.readlines()[0].strip()
    
    # input = input.split('\n\n')
            
    # input = ["" if x == '' else int(x) for x in input]
    input = utils.split_list(input, "")
    # input = [x for x in input]
    # input = [int(x) for x in input[0].split(',')]
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[int(s) for s in x] for x in input] # Parse a 2-d number grid


class Monkey():
    def __init__(self, monkey_input):
        self.m_id = int(monkey_input[0].split(" ")[1][0])
        self.items = [int(x) for x in monkey_input[1][(len("Starting items: ")):].split(',')]
        self.inspection_count = 0
        
        self.is_mul_step = False
        [op, val2] = monkey_input[2][len("Operation: new = old "):].split(' ')
        if val2 == 'old':
            if op == '+':
                self.fun = lambda x: x + x
                self.fun.__repr__ = lambda: "new = old + old"
            elif op == "*":
                self.fun = lambda x: x * x
                self.fun.__repr__ = lambda: "new = old * old"
                # self.is_mul_step = True
            else:
                throw
        else:
            if op == '+':
                self.fun = lambda x: x + int(val2)
                self.fun.__repr__ = lambda: "new = old + " + str(val2)
            elif op == '*':
                self.fun = lambda x: x * int(val2)
                self.fun.__repr__ = lambda: "new = old * " + str(val2)
                # self.is_mul_step = True
            else: 
                throw
        
        self.test = int(monkey_input[3][len("Test: divisible by "):])
        
        self.true_dest = int(monkey_input[4][len("If true: throw to monkey "):])
        self.false_dest = int(monkey_input[5][len("If false: throw to monkey "):])
    
    def do_step(self, monkeys, part1=False, debug=False):
        for item in self.items:
            if debug:
                print("\n--", self)
                print("Item: ", item)

            new_score = self.fun(item)
            
            if debug:
                print("After fun: ", new_score)
                
            self.inspection_count = self.inspection_count + 1

            if part1:
                new_score = math.floor(new_score / 3)
                if debug:
                    print("After reduce worry: ", new_score)
                    
            check = (new_score % self.test) == 0
            
            if debug:
                print("Check: ", check)
                
            if check:
                if debug:
                    print("Sending %d to: "%new_score, self.true_dest)
                monkeys[self.true_dest].items.append(new_score)
            else:
                if debug:
                    print("Sending %d to: "%new_score, self.false_dest)
                monkeys[self.false_dest].items.append(new_score)
        self.items = []
            
            
    def do_step_hack(self, monkeys, part1=False, debug=False):
        for item in self.items:
            if debug:
                print("\n--", self)
                print("Item: ", item)

            new_score = item
            if not self.is_mul_step:
                new_score = self.fun(item)
                
            if debug:
                print("After fun: ", new_score)
                
            self.inspection_count = self.inspection_count + 1

            if part1:
                new_score = math.floor(new_score / 3)
                if debug:
                    print("After reduce worry: ", new_score)
            else:
                # if new_score % self.big_number == 0:
                # print("Culling")
                new_score = new_score % self.big_number
                    
            check = (new_score % self.test) == 0
            
            if debug:
                print("Check: ", check)
                
            if check:
                if debug:
                    print("Sending %d to: "%new_score, self.true_dest)
                monkeys[self.true_dest].items.append(new_score)
            else:
                if debug:
                    print("Sending %d to: "%new_score, self.false_dest)
                monkeys[self.false_dest].items.append(new_score)
        self.items = []        
        
        
    def __repr__(self):
        return ("Monkey " + str(self.m_id) + \
            ": \n\t[" + ",".join([str(x) for x in self.items]) + "]" + \
            "\n\tfun: " + self.fun.__repr__()) + \
            "\n\tDivisble by: %d"%self.test + \
            "\n\tTrue - %d | False - %d"%(self.true_dest, self.false_dest)


def part1():
    # print(input)
    monkeys = []

    for monkey in input:
        m = Monkey(monkey)
        monkeys.append(m)
        print(m)
    print("\n\n")
        
    for i in range(20):
        for monkey in monkeys:
            monkey.do_step(monkeys, part1=True, debug=False)

    
        
    top_monkeys = sorted([x.inspection_count for x in monkeys])[::-1]
    return top_monkeys[0] * top_monkeys[1]
    
    
def part2():
    monkeys = []

    for monkey in input:
        m = Monkey(monkey)
        monkeys.append(m)
        print(m)
    print("\n\n")
    
    big_number = functools.reduce(operator.mul, [x.test for x in monkeys], 1)
    print(big_number)
    for monkey in monkeys:
        monkey.big_number = big_number
    
    for i in range(10000):
        for monkey in monkeys:
            monkey.do_step_hack(monkeys, part1=False, debug=False)
    print([x.inspection_count for x in monkeys])
    
    top_monkeys = sorted([x.inspection_count for x in monkeys])[::-1]
    return top_monkeys[0] * top_monkeys[1]
    
# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")