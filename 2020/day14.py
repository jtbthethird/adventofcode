import template
import copy
import re
import math
import numpy
from functools import reduce

filename="input14.txt"
# filename="testinput14.txt"

input = []
with open(filename) as f:
    input = f.readlines()
    # input = [int(x.strip()) for x in input]
    # input = [[z for z in x.strip()] for x in input]
    input = [x.strip() for x in input]

# --- #

def part1():
    
    mem = {}
    lineRE = "mem\[(\d+)\] = (\d+)"
    
    mask1 = ''.zfill(36)
    mask0 = ''.zfill(36)
    for inst in input:
        if inst.split(' ')[0] == 'mask':
            mask = inst.split(' ')[-1]
            # print("new mask: ", mask)
            mask1Str = mask.replace('X', '1')
            mask0Str = mask.replace('X', '0')
            mask1 = int(mask1Str, 2)
            mask0 = int(mask0Str, 2)
            continue
        
        m = re.match(lineRE, inst)
        # print(inst, m.groups())
        (reg, val) = m.groups()
        nVal = (int(val) & mask1) | mask0
        # print("inVal: %s\n mask: %s\nmask0: %s\nmask1: %s\n=nVal: %s\n----------"%( \
        #     bin(int(val))[2:].zfill(36), \
        #     mask, \
        #     bin(mask0)[2:].zfill(36), \
        #     bin(mask1)[2:].zfill(36), \
        #     bin(nVal)[2:].zfill(36)))
        # print("result: ", int(reg), nVal, bin(nVal))
        # print('==')
        mem[int(reg)] = nVal
    
    # print(mask, mem)
    return sum(mem.values())
    
def part2():
    mem = {}
    lineRE = "mem\[(\d+)\] = (\d+)"
    
    mask1 = ''.zfill(36)
    mask0 = ''.zfill(36)
    for inst in input:
        print("inst: ", inst)
        if inst.split(' ')[0] == 'mask':
            mask = inst.split(' ')[-1]
            # print("new mask: ", mask)
            # mask1Str = mask.replace('X', '1')
            mask0Str = mask.replace('X', '0')
            # mask1 = int(mask1Str, 2)
            mask0 = int(mask0Str, 2)
            continue
        m = re.match(lineRE, inst)
        # print(inst, m.groups())
        (reg, val) = m.groups()
        
        baseReg = bin(int(reg) | mask0)[2:].zfill(36)
        # print("Base Reg: ", baseReg)
        for i,v in enumerate(mask):
            if v == 'X':
                baseReg = baseReg[:i] + 'X' + baseReg[1+i:]
        # print("Base Reg: ", baseReg)
        
        regList = []
        xes = [v for v in baseReg if v == 'X']
        # print(len(xes), "->", 2**len(xes), bin(2**(len(xes))-1))
        for n in range(2**(len(xes))):
            newReg = copy.copy(baseReg)
            ostr = bin(n)[2:].zfill(len(xes))
            for x in ostr:
                newReg = newReg.replace('X', x, 1)
            # print("newReg", newReg)
            mem[int(newReg, 2)] = int(val)
    
    print(len(mem.values()))
    return sum(mem.values())
        

# --- #

if __name__ == "__main__":
    template.funWrapper(part1, "Part 1")
    template.funWrapper(part2, "Part 2")
