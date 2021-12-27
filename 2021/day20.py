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

day = 20

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
    input = [list(x) for x in input]


def pad_by(img, n, pad_with):
    return np.pad(img, ((n, n),(n,n)), 'constant', constant_values=(pad_with))
    

def enhance_image(img, mask):
    out = copy.copy(img)
    for y, row in enumerate(img[1:-1]):
        for x, val in enumerate(row[1:-1]):
            # print(x+1, y+1, val)
            m = img[[[y],[y+1],[y+2]],[x,x+1,x+2]]
            # print(m)
            s = [v for r in m for v in r]
            # print(s)
            
            bs = "".join(s).replace(".", "0").replace("#", "1")
            # print(bs)
            b = int(bs, 2)
            # print(b)
            nv = mask[b]
            # print(nv)
            out[y+1][x+1] = nv
            # print(x, y, nv)
    # print(out[0][0])
    width = len(img)
    height = len(img[0])
    if mask[0] == "#" and out[0][0] == ".":
        out[0] = np.full([1,width], "#")
        out[-1] = np.full([1,width], "#")
        out[:, 0] = np.full([1,height], "#")
        out[:, -1] = np.full([1,height], "#")
    elif mask[-1] == "." and out[0][0] == "#":
        out[0] = np.full([1,width], ".")
        out[-1] = np.full([1,width], ".")
        out[:, 0] = np.full([1,height], ".")
        out[:, -1] = np.full([1,height], ".")
    return out

def part1():
    steps = 2
    # print(input)
    mask = input[0]
    
    image = input[2:]
    img = np.array(image)
    img = pad_by(img, 2, ".")
    # utils.printMatrix(img)
    # print(img)
    
    utils.printMatrix(img)
    
    for i in range(steps):
        # print(i)
        edge = img[0][0]
        img = pad_by(img, 2, edge)
        img = enhance_image(img, mask)
        # utils.printMatrix(img)

    
    return sum([1 if c == "#" else 0 for row in img for c in row])
    
def part2():
    steps = 50
    # print(input)
    mask = input[0]
    
    image = input[2:]
    img = np.array(image)
    img = pad_by(img, 2, ".")
    # utils.printMatrix(img)
    # print(img)
    
    utils.printMatrix(img)
    
    for i in range(steps):
        print(i)
        edge = img[0][0]
        img = pad_by(img, 2, edge)
        img = enhance_image(img, mask)
    utils.printMatrix(img)

    
    return sum([1 if c == "#" else 0 for row in img for c in row])

# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")