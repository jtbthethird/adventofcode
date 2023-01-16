import utils
import time
import string
import copy
import math
import re
import heapq
import numpy as np
import os
from collections import Counter, defaultdict
from os import path

day = "07"

filename="input_"+str(day)+".txt"
# filename="test_"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    input = [l.strip() for l in f.readlines()] # One entry for each line
    # input = f.readlines()[0].strip()
    
    # input = input.split('\n\n')
            
    # input = ["" if x == '' else int(x) for x in input]
    # input = utils.split_list(input, "")
    # input = [x for x in input]
    # input = [int(x) for x in input[0].split(',')]
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[int(s) for s in x] for x in input]


# --- Parse the inputs ---
class Dir:
    def __init__(self, name):
        self.name = name
        self.files = []
        self.dirs = {}
        self.parent = None
        self.size = None
        
    def get_size(self):
        if self.size:
            return self.size
        child_sizes = sum([x.get_size() for x in self.dirs.values()])
        my_size = sum([x[1] for x in self.files])
        self.size = child_sizes + my_size
        return self.size

    def __repr__(self):
        depth = 0
        n = self.parent
        while n is not None:
            depth = depth + 1
            n = n.parent
        return ("  "*depth) + "- %s (dir)"%(self.name) + \
                "\n" + ("  "*depth) + "  - " + ("\n" + "  "*depth + "  - ").join(["%s (file, size=%d)"%(x[0], x[1]) for x in self.files]) + \
                "\n" + ("\n" + "  "*depth).join([d.__repr__() for d in self.dirs.values()])

def parse_ls_output(lines, node):
    while lines and lines[0][0] != '$':
        line = lines.pop(0)

        if line[:3] == "dir":
            # print("This is a dir")
            dir_name = line[4:]
            # print(dir_name)
            if dir_name not in node.dirs:
                newdir = Dir(dir_name)
                newdir.parent = node
                node.dirs[dir_name] = newdir
        else:
            [size, name] = line.split(' ')
            # print("Got file: ", name, int(size))
            node.files.append((name, int(size)))
    


def parse_command(lines, node):
    command = lines.pop(0)
    # print("This is a command")
    if command[2:4] == "cd":
        dest = command[5:]
        # print("change directory to ", dest)
        if node == None:
            new_dir = Dir(dest)
            # print(new_dir)
            return new_dir
        elif dest == "..":
            return node.parent
        else:
            if dest in node.dirs:
                return node.dirs[dest]
            else:
                print("Trying to CD to an unknown directory")
    elif command[2:4] == "ls":
        parse_ls_output(lines, node)
        return node
    

def parse_next_line(lines, node):
    # print("\n", lines[0])
    if lines[0][0] == '$':
        return parse_command(lines, node)
        
    return node


def get_directories(node, l=[]):
    l.append(node)
    for d in node.dirs.values():
        get_directories(d, l)
    return l

def part1():
    # print(input)
    lines = copy.copy(input)
    node = None
    
    while lines:
        node = parse_next_line(lines, node)

        # print(node)
        
    while node.parent is not None:
        node = node.parent
        
    print("---")    #
    print(node)
    #
    # print("---")
    dirs = get_directories(node)
    sizes = [d.get_size() for d in dirs]
    
    return sum([s for s in sizes if s <= 100000])
    
    
def part2():
    disk_space = 70000000
    space_needed = 30000000
    
    lines = copy.copy(input)
    
    
    node = None
    while lines:
        node = parse_next_line(lines, node)

        
    while node.parent is not None:
        node = node.parent
        
    total_size = node.get_size()
    print(total_size)
    
    unused_space = disk_space - total_size
    
    size_to_delete = space_needed - unused_space
    print("to delete", size_to_delete)
    
    dirs = get_directories(node)
    sizes = [d.get_size() for d in dirs]
    
    sizes.sort()
    
    for v in sizes:
        if v >= size_to_delete:
            return v

    
    return 0


# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")