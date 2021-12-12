import template
import copy
import regex as re
import math 
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


filename="input24.txt"
# filename="testinput24.txt"

input = []
with open(filename) as f:
    # input = [[int(x) for x in groups.split('\n')[1:]] for groups in f.read().split('\n\n')]
    input = f.readlines()
    
    # input = [int(x.strip()) for x in input[0].split(',')]
    # input = [[z for z in x.strip()] for x in input]
    input = [x.strip() for x in input]
    
# --- #
def parseLine(line):
    # dirs = []
    tok = [x for x in line]
    
    x = 0
    y = 0
    
    while len(tok) > 0:
        c1 = tok.pop(0)
        if c1 in ['s', 'n']:
            c2 = tok.pop(0)
            # dirs.append(c1+c2)
            if c1 == 's':
                y -= 1
            else:
                y+= 1
            if c2 == 'e':
                x += 0.5
            else:
                x -= 0.5
        else:
            # dirs.append(c1)
            if c1 == 'e':
                x += 1
            else:
                x -= 1

    return (x,y)
    
    

def part1():

    flips = set()
    for line in input:
        x,y = parseLine(line)
        
        if (x,y) in flips:
            flips.remove((x,y))
        else:
            flips.add((x,y))
    # print(flips)

    return len(flips)
    
def get_adjascent_count(pos, tiles):
    nw = (pos[0]-0.5, pos[1]+1)
    ne = (pos[0]+0.5, pos[1]+1)
    w =  (pos[0] - 1, pos[1])
    e =  (pos[0] + 1, pos[1])
    sw = (pos[0]-0.5, pos[1]-1)
    se = (pos[0]+0.5, pos[1]-1)
    adjs = [nw, ne, w, e, sw, se]
    out = 0
    for a in adjs:
        if a in tiles and tiles[a]:
            out += 1
    return out
    
    
def part2():
    tiles = {}
    for line in input:
        loc = parseLine(line)
        
        if loc in tiles:
            tiles[loc] = not tiles[loc]
        else:
            tiles[loc] = True
            
    days = 100    
    
    for day in range(days):
        xs = [x[0] for x in tiles.keys()]
        ys = [x[1] for x in tiles.keys()]
        minx = min(xs)
        miny = min(ys)
        maxx = max(xs)
        maxy = max(ys)
        next_tiles = copy.deepcopy(tiles)
        for y in range(int(miny)-1, int(maxy)+2):
            xrang = np.arange(math.floor(minx) - 2, math.ceil(maxx)+3)
            if y % 2 == 1:
                xrang = np.arange(math.floor(minx) - 1.5, math.ceil(maxx)+2.5)
                # print("odd y")
            # print(xrang)
            for x in xrang:
                count = get_adjascent_count((x, y), tiles)
                # print(count)
            
                v = False
                if (x,y) in tiles:
                    v = tiles[(x,y)]
                if v and (count == 0 or count > 2):
                    next_tiles[(x,y)] = False
                elif (not v) and count == 2:
                    next_tiles[(x,y)] = True

        print(len([x for x in next_tiles.values() if x]))
        tiles = next_tiles
            

    return len([x for x in tiles.values() if x])
    
# --- #

if __name__ == "__main__":
    template.funWrapper(part1, "Part 1")
    template.funWrapper(part2, "Part 2")

    
        