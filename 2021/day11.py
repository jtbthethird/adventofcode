import utils
import copy
import re
import numpy as np
from os import path

day = 11

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
    input = [[int(s) for s in x] for x in input]
    
class Cell:
    def __init__(self, val, x, y, left, up):
        self.x = x
        self.y = y
        self.left = left
        if left:
            left.right = self
        self.right = None
        self.up = up
        if up:
            up.down = self
        self.down = None
        self.val = val
        self.needs_to_flash = False
        self.flashing = False
        
    def reset_round(self):
        if self.flashing:
            self.flashing = False
            self.val = 0
    

    def inc_cell(self):
        if self.flashing:
            return
        else:
            self.val = self.val + 1
            if self.val == 10:
                self.needs_to_flash = True
        
    def flash(self):
        if self.flashing:
            return
        # print("Flashing! - (%d,%d)"%(self.x, self.y))
        self.flashing = True
        self.needs_to_flash = False
        neighbors = [self.left,  self.up, self.right, self.down]
        if self.up:
            neighbors.append(self.up.left)
            neighbors.append(self.up.right)
        if self.down:
            neighbors.append(self.down.left)
            neighbors.append(self.down.right)
            
        for n in neighbors:
            if n:
                n.inc_cell()
                
    def __str__(self):
        if self.flashing:
            return "*"
        return str(self.val)

        

def run_step(cells):
    # Increment all the cells (some will be val 10)
    # All the cells that are at 10 should flash
    # Reset the round - if flashing, set to zero and turn off
    straight_list = [cell for row in cells for cell in row]

# 
    # print([v.val for v in straight_list])
    
    for c in straight_list:
        c.val += 1
        if c.val == 10:
            c.needs_to_flash = True

    # print([v.val for v in straight_list])
    flashes = 0        
    
    ntf = [c for c in straight_list if c.needs_to_flash]
    # print([v.val for v in ntf])
    while ntf:
        for n in ntf:
            flashes += 1
            n.flash()
        ntf = [c for c in straight_list if c.needs_to_flash]
            

    # utils.printMatrix(cells)
    # print([v.val for v in straight_list])
    
    for c in straight_list:
        c.reset_round()
    
    return flashes
    
    

def part1():
    cycles = 100
    # utils.printMatrix(input)
    
    cells = []
    for y, row in enumerate(input):
        cell_row = []
        for x, val in enumerate(row):
            left = None
            up = None
            if cell_row:
                left = cell_row[-1]
            if cells:
                up = cells[y-1][x]
            cell = Cell(val, x, y, left, up)
            cell_row.append(cell)
            # print(cell)
        cells.append(cell_row)
    
    print()
    utils.printMatrix(cells)
            
    score = 0
    for i in range(cycles):
        # print("\n---- Step %d ---"%i)
        score += run_step(cells)
        print(score)
    
        # utils.printMatrix(cells)
    return score
    
    

    
    
def part2():
    # cycles = 200
    # utils.printMatrix(input)
    
    cells = []
    for y, row in enumerate(input):
        cell_row = []
        for x, val in enumerate(row):
            left = None
            up = None
            if cell_row:
                left = cell_row[-1]
            if cells:
                up = cells[y-1][x]
            cell = Cell(val, x, y, left, up)
            cell_row.append(cell)
            # print(cell)
        cells.append(cell_row)
    
    print()
    utils.printMatrix(cells)
            
    i = 0
    total_cells = len([c for row in cells for c in row])
    while True:
        i += 1
        print("\n---- Step %d ---"%i)
        score = run_step(cells)
        print("score: ", score)
        
        if (score == total_cells):
            return i
    
        
    

# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")