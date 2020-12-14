import template
import copy
import re
import math
import numpy
from functools import reduce

filename="input13.txt"
# filename="testinput13.txt"

input = []
with open(filename) as f:
    input = f.readlines()
    # input = [int(x.strip()) for x in input]
    # input = [[z for z in x.strip()] for x in input]
    input = [x.strip() for x in input]

# --- #

def part1():
    myTime = int(input[0])
    busTimes = [b for b in input[1].split(',') if b != 'x']
    # print(busTimes)
    bT = [int(b) - (myTime % int(b)) for b in busTimes]
    m  = min(bT)
    # print(bT, m)
    busId = int(busTimes[bT.index(m)])
    
    # print(busId)
    
    x = math.ceil(myTime / int(busId)) * int(busId)
    wait = (x - myTime)
    # print(wait)
    
    return wait * busId
    
def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def part2():
    # b1 * x = n
    # b2 * y = n + 1

    busTimes = [(int(b) - i,int(b)) for i,b in enumerate(input[1].split(',')) if b != 'x']

    print(busTimes)
    
    bigM = numpy.prod([m[1] for m in busTimes])

    acc = 0
    for b in busTimes:
        mi = b[1]
        bi = int(bigM / mi)
        ai = b[0]
        bpi = modinv(bi, mi)
        print(mi, bi, ai, bpi)
        mult = (ai * bi * bpi)
        print(acc, mult)
        acc += mult

    # print(acc)
    return (acc % bigM)
    # return 1

# --- #

if __name__ == "__main__":
    template.funWrapper(part1, "Part 1")
    template.funWrapper(part2, "Part 2")
