import utils
import copy
import re
import numpy as np
from os import path

day = 12

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
    
class Cell:
    def __init__(self, name):
        self.name = name
        self.links = []
        self.is_big = name.isupper()
    
    def add_link(self, other_cell):
        if other_cell in self.links:
            return
        self.links.append(other_cell)
        other_cell.add_link(self)
    
    def __str__(self):
        return "%s (big: %s)  - (%s)"%(self.name, self.is_big, ",".join([c.name for c in self.links]))
    


def find_paths_to_end(cell, path=[]):
    if not cell.is_big and cell in path:
        return None
    p2 = copy.copy(path)
    p2.append(cell)
    
    if cell.name == "end":
        return [p2]
    
    output = []
    for l in cell.links:
        new_paths = find_paths_to_end(l, p2)
        if new_paths is not None:
            output = output + new_paths
    return output
    

def get_cells():
    cells = {}
    for line in input:
        [c1, c2] = line.split("-")
        if c1 in cells:
            cell1 = cells[c1]
        else:
            cell1 = Cell(c1)
            cells[c1] = cell1
        
        if c2 in cells:
            cell2 = cells[c2]
        else:
            cell2 = Cell(c2)
            cells[c2] = cell2
            
        cell1.add_link(cell2)
    return cells
        

def part1():
    cells = get_cells()
    
    out = find_paths_to_end(cells["start"])
    # for path in out:
    #     print(",".join([c.name for c in path]))

    return len(out)

    
def dfs_2(cell, path=[], hit_sm_twice=False):
    if cell.name == "start" and len(path) > 0:
        return None
            
    p2 = copy.copy(path)
    p2.append(cell)
    
    if cell.name == "end":
        return [p2]
    
    if not cell.is_big:
        # This is a small cave
        if cell in path:
            if hit_sm_twice:
                # We've already used our allotted 2 visits to a cell
                return None
            # We haven't used our two visits, but this is now a second visit
            # print("--- Hitting a cell twice (%s) --"%cell.name)
            # print("Path so far: ", [c.name for c in path])
            hit_sm_twice = True
            
    
    output = []
    for l in cell.links:
        new_paths = dfs_2(l, p2, hit_sm_twice)
        if new_paths is not None:
            output = output + new_paths
    return output

def part2():
    cells = get_cells()
    
    out = dfs_2(cells["start"])
    return len(out)
    

# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")