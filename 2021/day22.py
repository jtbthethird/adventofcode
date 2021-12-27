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

day = 22

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
    
class Cube():
    def __init__(self, ranges, on=True):
        [self.x_range, self.y_range, self.z_range] = ranges
        self.minx = min(self.x_range)
        self.maxx = max(self.x_range)
        self.miny = min(self.y_range)
        self.maxy = max(self.y_range)
        self.minz = min(self.z_range)
        self.maxz = max(self.z_range)
        self.x_dist = self.maxx - self.minx
        self.y_dist = self.maxy - self.miny
        self.z_dist = self.maxz - self.minz
        self.on = on

    def __str__(self):
        return "(%d..%d, %d..%d, %d..%d) - %s"%(self.x_range[0], self.x_range[1], self.y_range[0], self.y_range[1], self.z_range[0], self.z_range[1], self.on)
        
    def __repr__(self):
        return self.__str__()

    def volume(self):
        return self.x_dist * self.y_dist * self.z_dist
        
        
    def intersects(self, other):
        return ((max(self.x_range) > min(other.x_range) and min(self.x_range) < max(other.x_range)) and 
            (max(self.y_range) > min(other.y_range) and min(self.y_range) < max(other.y_range)) and
            (max(self.z_range) > min(other.z_range) and min(self.z_range) < max(other.z_range)))
        
    def subtract(self, other):
        """ Return a list of cubes that equals (self - other) """
        if not self.intersects(other):
            return [self]
            
        # What we really want to do is just subtract the intersection cube
        x1 = max(self.minx, other.minx)
        x2 = min(self.maxx, other.maxx)
        y1 = max(self.miny, other.miny)
        y2 = min(self.maxy, other.maxy)
        z1 = max(self.minz, other.minz)
        z2 = min(self.maxz, other.maxz)
            
        other = Cube([[x1,x2],[y1,y2],[z1,z2]])
        
        # In 2d this looks like:
        # 
        # __________________
        # |                   |
        # |      A            |
        # |   ____________    |
        # | B |           |C  |
        # |   |___________|   |
        # |                   |
        # |         D         |
        # |___________________|
        #
        # Which is 
        #   A = (self.minx, self.miny) to (self.maxx, other.miny)
        #   B = (self.minx, other.miny) to (other.minx, other.maxy)
        #   C = (other.maxx, other.miny) to (self.max, other.maxy)
        #   D = (self.minx, other.maxy) to (self.maxx, self.maxy)
        
        # Then, if any dimension is zero, delete that box
        
        # In 3d this should just add 2 more boxes (one front, one back)
        # So all of those would have z = other.minz to other.maxz
        # And we'd add 
        #.  E = (self.minx, self.miny, self.minz) to (self.maxx, self.maxy, other.minz)
        #   F = (self.minx, self.miny, other.maxz) to (self.maxx, self.maxy, self.maxz)
        
        a = Cube([[self.minx, self.maxx],[self.miny, other.miny],[other.minz, other.maxz]])
        b = Cube([[self.minx, other.minx],[other.miny, other.maxy], [other.minz, other.maxz]])
        c = Cube([[other.maxx, self.maxx],[other.miny, other.maxy], [other.minz, other.maxz]])
        d = Cube([[self.minx, self.maxx],[other.maxy, self.maxy], [other.minz, other.maxz]])
        e = Cube([[self.minx, self.maxx],[self.miny, self.maxy],[self.minz, other.minz]])
        f = Cube([[self.minx, self.maxx], [self.miny, self.maxy],[other.maxz, self.maxz]])
        
        all_cubes = [a,b,c,d,e,f]
        
        output = [cube for cube in all_cubes if cube.volume() > 0]
            
        return output
    
def part1():
    # print(input)
    a = np.array(utils.make3dArray(101, 101, 101))
    # print(a)
    for line in input:
        [on_str, nums] = line.split(" ")
        v = 1 if on_str == "on" else 0
        r = [[int(v) + 50 for v in rv[2:].split("..")] for rv in nums.split(",")]
        
        if not np.all([val <= 101 for val in np.abs(r)]):
            # print("no dice")
            continue
            
        a[r[2][0]:r[2][1]+1,r[1][0]:r[1][1]+1,r[0][0]:r[0][1]+1] = v
        # print("line", v, r)
        # print()
        # print(a[r[2][0]:r[2][1],r[1][0]:r[1][1],r[0][0]:r[0][1]])
        # print(np.sum(a))
    
    return np.sum(a)
    
    
def part2_test():
    c1 = Cube([[0,10],[0,10],[0,10]])
    print(c1, c1.volume())
    
    cut = Cube([[1,11],[-1,11],[-1, 11]])
    # empty = c1.subtract(cut)
    # print(c1.subtract(cut))
    # print(cut.subtract(c1))
    # print(c1.volume(), cut.volume(), sum([x.volume() for x in cut.subtract(c1)]))
    
def part2():
    # print(input)
    cubes = []
    for line in input:
        [on_str, nums] = line.split(" ")
        on = on_str == "on"
        r = [[int(v) for v in rv[2:].split("..")] for rv in nums.split(",")]
        r  = [[v[0], v[1]+1] for v in r]
        c = Cube(r, on)
        cubes.append(c)
    
    # print(cubes)
    # print("-----")
    new_cubes = [cubes[0]]
    i = 0
    # print("After step %d - total lights on is %d"%(i, sum([x.volume() for x in new_cubes])))
    for c in cubes[1:]:
        i += 1
        # print("Flipping the lights: ", c)
        # If c is an off:
        #   Return all other cubes - c
        if c.on:    
            # print("Turning some lights on")
            # If c is an "on"
            # Go through all the already existing cubes
            # Subtract the existing cubes from c -> get a new list of cubes
            # Repeat for all the broken down cubes against each existing cube
            cubes_to_add = [c]
            for existing_cube in new_cubes:
                cubes_to_add_2 = []
                for cta in cubes_to_add:
                    cta_split = cta.subtract(existing_cube)
                    cubes_to_add_2 = cubes_to_add_2 + cta_split
                cubes_to_add = cubes_to_add_2
            new_cubes = new_cubes + cubes_to_add
            # print(new_cubes)
        else:
            # If c is an "off"
            # new_cubes_2 is an empty list
            # For each cube in new_cubes_2, subtract c and add the result to the new list
            # Replace new_cubes with new_cubes_2 at the end
            new_cubes_2 = []
            for existing_cube in new_cubes:
                cubes_minus_c = existing_cube.subtract(c)
                new_cubes_2 = new_cubes_2 + cubes_minus_c
            new_cubes = new_cubes_2
        # print("After step %d - total lights on is %d"%(i, sum([x.volume() for x in new_cubes])))
    
    return sum([x.volume() for x in new_cubes])
            
        
            
    
    


# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")