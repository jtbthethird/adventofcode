import utils
import time
import copy
import math
import re
import heapq
import numpy as np
import os
from os import path

day = 16

filename="input"+str(day)+".txt"
# filename="testinput"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    input = [l.strip() for l in f.readlines()][0] # One entry for each line
    
    # input = [x for x in input]
    # input = [int(x) for x in input[0].split(',')]
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[int(s) for s in x] for x in input]
        
class Packet:    
    def __init__(self, ptype, version):
        self.ptype = ptype
        self.version = version
        self.subpackets = []
        self.value = None
        
    def add_subpacket(self, subpacket):
        self.subpackets.append(subpacket)
    
    def get_version_total(self):
        return sum([s.get_version_total() for s in self.subpackets]) + self.version
        
        
    def str_2(self):
        # print("self.ptype: ", self.ptype)
        if self.ptype == 0:
            return "(%d = (%s))"%(self.value, " + ".join([x.str_2() for x in self.subpackets]))
        elif self.ptype == 1:
            return "(%d = (%s))"%(self.value, " * ".join([x.str_2() for x in self.subpackets]))
        elif self.ptype == 2:
            return "(%d = min(%s))"%(self.value, ", ".join([x.str_2() for x in self.subpackets]))
        elif self.ptype == 3:
            return "(%d = max(%s))"%(self.value, ", ".join([x.str_2() for x in self.subpackets]))
        elif self.ptype == 4:
            return "%d"%self.value
        elif self.ptype == 5:
            return "(%s > %s)"%(self.subpackets[0].str_2(), self.subpackets[1].str_2())
        elif self.ptype == 6:
            return "(%s < %s)"%(self.subpackets[0].str_2(), self.subpackets[1].str_2())
        elif self.ptype == 7:
            return "(%s == %s)"%(self.subpackets[0].str_2(), self.subpackets[1].str_2())
            
    def __str__(self):
        base_str = "{ version: %d, type: %d"%(self.version, self.ptype)
        if self.value:
            base_str += ", value: %d"%self.value
        if self.subpackets:
            child_str = ", children: [%s]"%(",".join([s.__str__() for s in self.subpackets]))
            base_str += child_str
        base_str += " }"

        return base_str
        

def get_literal(p):
    s = p[0]
    n = ""
    while s != "0":
        n += p[1:5]
        p = p[5:]
        s = p[0]
    n += p[1:5]
    p = p[5:]
    return (int(n, 2), p)    

def decode_packet(p):
    v = int(p[0:3], 2)
    p = p[3:]
    
    t = int(p[0:3], 2)
    p = p[3:]
    
    packet = Packet(t, v)
    
    if t == 4:
        (l, p) = get_literal(p)
        packet.value = l
    else:
        i = int(p[0])
        if i == 0:
            length = int(p[1:16], 2)
            p=p[16:]
            sub_p = p[:length]
            while sub_p:
                [d, sub_p] = decode_packet(sub_p)
                packet.add_subpacket(d)
            p = p[length:]
        elif i == 1:
            l = int(p[1:12], 2)
            p = p[12:]
            for i in range(l):
                [d, p] = decode_packet(p)
                packet.add_subpacket(d)
    # Calculate value
    sub_values = [x.value for x in packet.subpackets]
    if t == 0:
        packet.value = sum(sub_values)
    elif t == 1:
        packet.value = math.prod(sub_values)
    elif t == 2:
        packet.value = min(sub_values)
    elif t == 3:
        packet.value = max(sub_values)
    elif t == 5:
        if sub_values[0] > sub_values[1]:
            packet.value = 1
        else:
            packet.value = 0
    elif t == 6:
        if sub_values[0] < sub_values[1]:
            packet.value = 1
        else:
            packet.value = 0
    elif t == 7:
        if sub_values[0] == sub_values[1]:
            packet.value = 1
        else:
            packet.value = 0
        
    return (packet, p)

def part1():
    h = input
    print(input)
    h_size = len(h) * 4
    s = bin(int(h, 16))[2:].zfill(h_size)
    (d, remainder) = decode_packet(s)
    print("Result: ", d)
    
    return d.get_version_total()
    

def part2():    
    h = input
    h_size = len(h) * 4
    s = bin(int(h, 16))[2:].zfill(h_size)
    (d, remainder) = decode_packet(s)
    print("Result: ", d.str_2())
    
    return d.value


# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")