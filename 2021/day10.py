import utils
import copy
import re
import numpy as np
from os import path

day = 10

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

char_score = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}    

autocomplete_score = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4
}

opens = ["(", "{", "<", "["]
closes = [")", "}", ">", "]"]
matches = {
    "(": ")",
    "{": "}",
    "[": "]",
    "<": ">"
}

def get_score_for_line(line):
    l2 = copy.copy(line)
    
    stack = []
    
    while l2:
        c = l2.pop(0)

        if c in opens:
            stack.append(c)
        elif len(stack) == 0:
            return char_score[c]
        else: 
            top = stack[-1]
            if matches[top] == c:
                stack.pop(-1)
            else:
                return char_score[c]
            
        # print (c, stack)
    
    return 0
        
        

def part1():    
    scores = 0
    for line in input:
        line_array = list(line)
        
        s = get_score_for_line(line_array)
        # print("%s ---- \n Score: "%line ,s)
        scores += s

    return scores
    



def get_autocomplete_score_for_line(line):
    l2 = copy.copy(line)
    
    stack = []
    
    while l2:
        c = l2.pop(0)

        if c in opens:
            stack.append(c)
        elif len(stack) == 0:
            return char_score[c]
        else: 
            top = stack[-1]
            if matches[top] == c:
                stack.pop(-1)
            else:
                return 0

    # Calculate the score to autocomplete
    # print(stack)
    stack.reverse()
    # print(stack)
    score = 0
    for c in stack:
        score = score * 5
        score += autocomplete_score[c]
        # print(c, score)
    return score
    
    
def part2():

    scores = []
    for line in input:
        line_array = list(line)
        
        s = get_autocomplete_score_for_line(line_array)
        
        # print(line, s)
        if s != 0: 
            scores.append(s)
    
    scores.sort()
    return scores[len(scores) // 2]
        
    

# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")