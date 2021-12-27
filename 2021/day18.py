import utils
import time
import copy
import math
import re
import heapq
import numpy as np
import os
from os import path

day = 18

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
    
    
class SnailfishNumber:
    def __init__(self):
        self.left = None
        self.right = None
        self.parent = None
        
    def __str__(self):
        return "[%s,%s]"%(self.left, self.right)
        
    def __repr__(self):
        return self.__str__()
        
    def set_left(self, num):
        self.left = num
        if type(num) is not int:
            num.parent = self
            num.is_left = True
            num.is_right = False
        
    def set_right(self, num):
        self.right = num
        if type(num) is not int:
            num.parent = self
            num.is_left = False
            num.is_right = True
            
    def add_to_next_left_num(self, add):
        if self.parent is None:
            return
        if self.is_left:
            self.parent.add_to_next_left_num(add)
        else:
            if type(self.parent.left) is int:
                self.parent.left += add
                return
            else:
                node = self.parent.left
                while type(node.right) is not int:
                    node = node.right
                node.right += add
                return

    def add_to_next_right_num(self, add):
        if self.parent is None:
            return
        if self.is_right:
            self.parent.add_to_next_right_num(add)
        else:
            if type(self.parent.right) is int:
                self.parent.right += add
                return
            else:
                node = self.parent.right
                while type(node.left) is not int:
                    node = node.left
                node.left += add
                return
    
    def should_explode(self, depth=0):
        if depth == 4:
            return True
        if isinstance(self.left, SnailfishNumber):
            if self.left.should_explode(depth + 1):
                return True
        if isinstance(self.right, SnailfishNumber):
            if self.right.should_explode(depth + 1):
                return True
        return False
        
    def explode(self, depth=0):
        if depth == 4:
            # print("exploding")
            self.add_to_next_left_num(self.left)
            self.add_to_next_right_num(self.right)
            if self.is_left:
                self.parent.left = 0
            else:
                self.parent.right = 0
            return True
        if isinstance(self.left, SnailfishNumber):
            exploded = self.left.explode(depth + 1)
            if exploded:
                return True
        if isinstance(self.right, SnailfishNumber):
            return self.right.explode(depth + 1)
        return False
        
    def should_split(self):
        if type(self.left) is int:
            if self.left >= 10:
                return True
        else:
            if self.left.should_split():
                return True
        if type(self.right) is int:
            if self.right >= 10:
                return True
        else:
            if self.right.should_split():
                return True
        return False

    def split(self):
        if type(self.left) is int:
            if self.left >= 10:
                # print("splitting left")
                n = SnailfishNumber()
                n.set_left(self.left // 2)
                n.set_right(math.ceil(self.left / 2))
                self.set_left(n)
                return True
        else:
            splitted = self.left.split()
            if splitted:
                return True
        
        if type(self.right) is int:
            if self.right >= 10:
                # print("splitting right")
                n = SnailfishNumber()
                n.set_left(self.right // 2)
                n.set_right(math.ceil(self.right / 2))
                self.set_right(n)
                return True
        else:
            return self.right.split()
        return False
        
    def sn_reduce(self):
        has_action = self.should_explode() or self.should_split()
        while has_action:
            if self.should_explode():
                self.explode()
            else:
                self.split()
            has_action = self.should_explode() or self.should_split()
            # print(self)
        return self

    def add(self, other):
        out = SnailfishNumber()
        out.set_left(self)
        out.set_right(other)
        return out
    
    def magnitude(self):
        l = 0
        r = 0
        if type(self.left) is int:
            l = self.left
        else:
            l = self.left.magnitude()
        if type(self.right) is int:
            r = self.right
        else:
            r = self.right.magnitude()
        return (3 * l) + (2 * r)
        
    
def parse_num(s):
    c = s[0]
    s = s[1:]
    
    if c == "[":
        n = SnailfishNumber()
        (nl, s) = parse_num(s)
        n.set_left(nl)

        comma = s[0]
        if comma != ",":
            print(s)
            raise Error("WTF")
            
        s = s[1:]
        
        (nr, s) = parse_num(s)
        n.set_right(nr)
        
        close = s[0]
        if close != "]":
            print(s)
            raise Error("WTF 2")
        s = s[1:]
        return (n, s)
    elif c in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
        n = int(c)
        return (n, s)
    

def part1():
    # print(input)
    
    snail_nums = [parse_num(s)[0] for s in input]

    cum = snail_nums[0]
    # print(cum)
    cum.sn_reduce()
    
    for n in snail_nums[1:]:
        # print(n)
        cum = cum.add(n)
        cum.sn_reduce()

    print("result: ")
    print(cum)
        
    return cum.magnitude()
    
    
def part2():
    # snail_nums = [parse_num(s)[0] for s in input]
    
    biggest = 0
    big_l = 0
    big_r = 0
    for i in range(len(input)-1):
        for j in range(i+1, len(input)):
            # print(i, j)
            n1 = parse_num(input[i])[0]
            n2 = parse_num(input[j])[0]
            # print(n1, n2)
            
            n3 = n1.add(n2).sn_reduce()
            # print("%s + %s = %s"%(n1, n2, n3))
            # print(n3.magnitude())
            if n3.magnitude() > biggest:
                big_l = i
                big_r = j
                biggest = n3.magnitude()
            

            n1 = parse_num(input[i])[0]
            n2 = parse_num(input[j])[0]
            n4 = n2.add(n1).sn_reduce()
            # print("%s + %s = %s"%(n2, n1, n4))
            # print(n4.magnitude())
            if n4.magnitude() > biggest:
                big_l = j
                big_r = i
                biggest = n4.magnitude()

    n1 = parse_num(input[big_l])[0]
    n2 = parse_num(input[big_r])[0]   
    
    print("%s + %s"%(n1, n2))
    print("=")
    print(n1.add(n2).sn_reduce())
    
    return biggest


# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")