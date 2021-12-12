import template
import copy
import re
import math
import numpy as np
import plotly.express as px

filename="input18.txt"
# filename="testinput18.txt"

input = []
with open(filename) as f:
    input = f.readlines()
    # input = [int(x.strip()) for x in input[0].split(',')]
    # input = [[z for z in x.strip()] for x in input]
    input = [x.strip() for x in input]

# --- #
digits = [i for i in range(10)]
digitStrs = [str(i) for i in digits]
ops = ['+', '*']


def numFromParenStr(pStr):
    reg = "\(*(\d+)\)*"
    n = re.findall(reg, pStr)
    return n[0]

def reduceParens(vals):
    # Iterate through all the vals, replace an entire parens section with a number
    closes = [i for i,v in enumerate(vals) if v.endswith(')')]
    if len(closes) == 0:
        return vals
        
    closeIdx = min(closes)

    openIdx = max([i for i,v in enumerate(vals) if v.startswith('(') and i < closeIdx])
    # print(openIdx, closeIdx)
    
    subVals = vals[openIdx:closeIdx+1]
    
    subVals[0] = numFromParenStr(subVals[0])
    subVals[-1] = numFromParenStr(subVals[-1])

    exp = evaluateExpression(subVals)
    
    openStr = vals[openIdx][:-(1+len(subVals[0]))]
    # print("opn: ", openStr, vals[openIdx], subVals[0])
    closeStr = vals[closeIdx][(1+len(subVals[-1])):]
    # print("cls: ", closeStr, vals[closeIdx], subVals[-1])
    v = openStr + str(exp) + closeStr
    
    newVals = vals[:openIdx] + [v] + vals[closeIdx+1:]
    
    # print(newVals)
    return reduceParens(newVals)
    
def reduceAdds(vals):
    adds = [i for i,v in enumerate(vals) if v == '+']
    if len(adds) == 0:
        return vals
    firstAdd = min(adds)
    subVals = vals[firstAdd-1:firstAdd+2]
    # print(subVals)
    
    newVal = int(subVals[0]) + int(subVals[-1])
        
    newVals = vals[:firstAdd-1] + [newVal] + vals[firstAdd+2:]
    
    # print("New vals: ", newVals)
    
    return reduceAdds(newVals)
        

def evaluateExpression(vals):
    vals = reduceParens(vals)

    vals = reduceAdds(vals)
    
    output = 0
    oper = "+"
    for val in vals:
        # print("val: ", val)
        if val in ops:
            # print("got op: ", val)
            oper = val
        else:
            # print("Doing math")
            if oper == "+":
                output += int(val)
            elif oper == "*":
                output *= int(val)
            else:
                print("WTF!")
        # print("output is now: ", output)
    return output

def evaluateLine(vals):
    return evaluateExpression(vals)
    

def part1():
    # print(input)
    # vals = input[1].split(' ')
    x = 0
    # x = evaluateExpression(input[0].split(' '))
    for line in input:
        vals = line.split(' ')
        y = evaluateLine(vals)
        # print(line, y)
        x += y
    # numFromParenStr("11)")
    
    
    return x
    
def part2():
    return 2

# --- #

if __name__ == "__main__":
    template.funWrapper(part1, "Part 1")
    template.funWrapper(part2, "Part 2")

    
    