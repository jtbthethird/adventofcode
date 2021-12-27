import utils
import copy
import re
import numpy as np
from os import path

day = 14

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

def part1():
    # print(input)
    
    steps = 10
    
    polymer = input[0]
    rules = {line.split(" -> ")[0]:line.split(" -> ")[1] for line in input[2:]}

    # print(polymer, rules)
    
    for s in range(steps):
        new_poly = copy.copy(polymer)
        for i in range(len(polymer)-1):
            lookup = polymer[i:i+2]
            c = rules[lookup]
            # print(i, lookup, c)
            new_poly = new_poly[:i*2+1] + c + new_poly[i*2+1:]
        print(new_poly)
        polymer = new_poly
    # print(polymer)
    counts = {}
    for c in polymer:
        if c in counts:
            counts[c] += 1
        else:
            counts[c] = 1
    
    print(counts)
    
    biggest = max(counts, key=counts.get)
    smallest = min(counts, key=counts.get)
    print(biggest, counts[biggest])
    print(smallest, counts[smallest])
    
    return counts[biggest] - counts[smallest]

def add_dicts(a, b):
    return {key: a.get(key, 0) + b.get(key, 0) for key in set(a) | set(b)}

class Node:
    def __init__(self, root, new_char):
        self.root = root
        self.new_char = new_char
        
    def get_counts(self, depth, memo={}):
        if depth == 1:
            return {self.new_char: 1}
            
        l = 0
        if (self.left.root, depth-1) in memo:
            l = memo[(self.left.root, depth-1)]
        else:
            l = self.left.get_counts(depth-1, memo)
            memo[(self.left.root, depth-1)] = l
        
        r = 0
        if (self.right.root, depth-1) in memo:
            r = memo[(self.right.root, depth-1)]
        else:
            r = self.right.get_counts(depth-1, memo)
            memo[(self.right.root, depth-1)] = r
        
        kids = add_dicts(l, r)
        if self.new_char in kids:
            kids[self.new_char] += 1
        else:
            kids[self.new_char] = 1
        # print(kids)
        return kids
        
        
    def __str__(self):
        return "%s -> %s"%(self.root, self.new_char)
        
    def __repr__(self):
        return self.__str__()

def get_graph():
    rules = {line.split(" -> ")[0]:line.split(" -> ")[1] for line in input[2:]}
    
    # print(rules)

    nodes = {k: Node(k, v) for (k,v) in rules.items()}
    
    for node in nodes.values():
        l = node.root[0] + node.new_char
        r = node.new_char + node.root[1]
        node.left = nodes[l]
        node.right = nodes[r]
    
    return nodes
        
    

def part2():
    depth = 40
    polymer = input[0]
    print(polymer)
    
    g = get_graph()
    
    counts = {k[0]: 0 for k in g.keys()}
    for c in polymer:
        counts[c] += 1
    
    for i in range(len(polymer)-1):
        root_node = polymer[i:i+2]
        node = g[root_node]
        counts = add_dicts(counts, node.get_counts(depth))
    
    print(counts)
    
    biggest = max(counts, key=counts.get)
    smallest = min(counts, key=counts.get)
    print(biggest, counts[biggest])
    print(smallest, counts[smallest])
    
    return counts[biggest] - counts[smallest]


# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")