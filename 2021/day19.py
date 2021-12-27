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

day = 19

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
    
class Beacon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.d_sqs = []
        
    def __str__(self):
        return "(%d, %d, %d)"%(self.x, self.y, self.z)
        
    def d_squared_to(self, other):
        return (self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2
        
    def shared_distances(self, other):
        c = list((Counter(self.d_sqs) & Counter(other.d_sqs)).elements())
        # print(c)
        # if len(c)>10:
            # print(c)
        return len(c)
    
    def array_value(self):
        return np.array([self.x,self.y,self.z])
        
    def get_vector_to(self, other):
        return [other.x - self.x, other.y - self.y, other.z - self.z]
        
    def get_relative_vecs(self, peers):
        return [self.get_vector_to(p) for p in peers]
        
    def rotate(self, transpose_matrix):
        new_a = self.array_value() @ transpose_matrix
        self.x = new_a[0]
        self.y = new_a[1]
        self.z = new_a[2]
        
    def translate(self, translation_vector):
        new_a = self.array_value() + translation_vector
        self.x = new_a[0]
        self.y = new_a[1]
        self.z = new_a[2]       
        
    # def __sub__(self, other):
        
            
def all_rotations():
    i = np.array([[1, 0, 0],[0, 1, 0],[0, 0, 1]])
    
    roll = np.array([[1, 0, 0],[0, 0, 1],[0, -1, 0]]) # roll top to face away from you - rolls around x-axis
    turn = np.array([[0, 0, 1],[0, 1, 0],[-1, 0, 0]]) # Turn anti-clockwise - turn around y-axis
    
    transforms = []
    
    last = i
    # transforms.append(last)
    for r in range(3):
        for t in range(3):
            last = last @ turn
            transforms.append(last)
        last = last @ roll
        transforms.append(last)
        
    last = last @ roll @ turn @ roll
    

    for r in range(3):
        for t in range(3):
            last = last @ turn
            transforms.append(last)
        last = last @ roll
        transforms.append(last)
    
    return transforms
    # Add initial
    # Turn 3 times
    # Roll
    # Turn 3 times
    

class Scanner:
    def __init__(self, num):
        self.num = num
        self.beacons = []
        self.location = np.array([0,0,0])
        
    def __str__(self):
        return ("Beacon %d (%s): [%s]"%(self.num, self.location, ", ".join([s.__str__() for s in self.beacons])))
        
    def __repr__(self):
        return self.__str__()
        
    def calc_distances(self):        
        # print(len(self.beacons))
        for i in range(len(self.beacons)-1):
            bi = self.beacons[i]
            for j in range(i+1, len(self.beacons)):
                bj = self.beacons[j]
                d_sq = bi.d_squared_to(bj)
                bi.d_sqs.append(d_sq)
                bj.d_sqs.append(d_sq)
        
    def rotate(self, transpose_matrix):
        for b in self.beacons:
            b.rotate(transpose_matrix)
            
    def translate(self, translation_vector):
        for b in self.beacons:
            b.translate(translation_vector)
        self.location = translation_vector
        
    def manhattan_distance_to(self, other):
        # print(other.location, self.location)
        diff = other.location - self.location
        dist = sum([abs(x) for x in diff])
        # print(dist)
        return dist
            
    
    def align_other_to_self(self, other):
        # This beacon overlaps with another if 12 of the Beacons are the same
        my_matching_beacons = []
        their_matching_beacons = []
        # To find this, check if any single beacon in my list has 12 overlapping d_sqs with any beacon in their list
        for mybeacon in self.beacons:
            for theirbeacon in other.beacons:
                # print("Checking: ", mybeacon, theirbeacon)
                x = mybeacon.shared_distances(theirbeacon)
                if x > 10:
                    # print("Found one!!", x, mybeacon, theirbeacon)
                    my_matching_beacons.append(mybeacon)
                    # my_matching_beacons = np.concatenate((my_matching_beacons, np.array()))
                    their_matching_beacons.append(theirbeacon)
        if len(my_matching_beacons) > 10:
            my_vecs = my_matching_beacons[0].get_relative_vecs(my_matching_beacons[1:])
            their_vecs = their_matching_beacons[0].get_relative_vecs(their_matching_beacons[1:])
            
            my_a = np.array(my_vecs)
            their_a = np.array(their_vecs)

            ts = all_rotations()
            
            for t in ts:
                check = their_a @ t
                # print(check)
                if np.array_equal(my_a, check):
                    # print("wtf", check, t)
                    break
            # print(t)
            
            my_b0 = my_matching_beacons[0]
            their_b0 = their_matching_beacons[0]
                        
            other.rotate(t)
                        
            translation = my_b0.array_value() - their_b0.array_value()
            # print(translation)
            other.translate(translation)

            return True
        else:
            return None
    

def parse_input():
    scanners = []
    s = None
    for line in input:
        if line[:3] == "---":
            n = int(line.split(" ")[2])
            # print(n)
            s = Scanner(n)
        elif line == "":
            # print(s)
            scanners.append(s)
            s = None
        else:
            [x,y,z] = [int(v) for v in line.split(",")]
            p = Beacon(x, y, z)
            s.beacons.append(p)

    scanners.append(s)
    # print(s)
    return scanners
        


def orient_scanners():

    scanners = parse_input()
    # print(scanners)
    
    for scanner in scanners:
        scanner.calc_distances()
    
    
    queue = [scanners[0]]
    
    disoriented_scanners = scanners[1:]
    
    while queue:
        o = queue.pop()
        still_disoriented = []
        for d in disoriented_scanners:
            did_realign = o.align_other_to_self(d)
            if did_realign:
                queue.append(d)
                # print()
                # print("Realigned!", d)
            else:
                still_disoriented.append(d)
        disoriented_scanners = still_disoriented
    return scanners

def part1():
    scanners = orient_scanners()
    
    out_set = set()
    for s in scanners:
        for b in s.beacons:
            out_set.add((b.x,b.y,b.z))
    
    return len(out_set)
    
def part2():
    scanners = orient_scanners()
    
    print("Lenght: ", len(scanners))
    max_dist = 0
    for i in range(len(scanners)-1):
        for j in range(i+1, len(scanners)):
            print(i,j)
            a = scanners[i]
            b = scanners[j]
            dist = a.manhattan_distance_to(b)

            print(a.location, b.location)
            print(a.location - b.location)
            print(abs(dist))

            if abs(dist) > max_dist:
                max_dist = abs(dist)
    
    return max_dist


# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")