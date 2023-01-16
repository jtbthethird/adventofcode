import utils
import time
import string
import itertools
import copy
import math
import regex
import re
import heapq
import numpy as np
import os
from collections import Counter, defaultdict
from os import path
import functools
import operator
import json
import matplotlib.pyplot as plt

day = "19"

filename="input_"+str(day)+".txt"
filename="test_"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    input = [l.strip() for l in f.readlines()] # One entry for each line
# filename="test_"+str(day)+".txt"
#     input = [c for c in input[0]]
    # input = [(x.split(' ')[0], int(x.split(' ')[1])) for x in input]
    # input = f.readlines()[0].strip()
    
    # input = input.split('\n\n')
            
    # input = ["" if x == '' else int(x) for x in input]
    # input = utils.split_list(input, "")
    # input = [x for x in input]
    # input = [int(x) for x in input[0].split('')]
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[int(s) for s in x] for x in input] # Parse a 2-d number grid
    # input = [tuple([int(v) for v in row.split(',')]) for row in input]


class Blueprint:
    def __init__(self, line):
        r = r'Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.'
        m = re.match(r, line)
        
        (_id, ore_cost_in_ore, clay_cost_in_ore, obsidian_cost_in_ore, obsidian_cost_in_clay, geode_cost_in_ore, geode_cost_in_obsidian) = m.groups()
        
        self._id = int(_id)
        self.ore_cost_in_ore = int(ore_cost_in_ore)
        self.clay_cost_in_ore = int(clay_cost_in_ore)
        self.obsidian_cost_in_ore = int(obsidian_cost_in_ore)
        self.obsidian_cost_in_clay = int(obsidian_cost_in_clay)
        self.geode_cost_in_ore = int(geode_cost_in_ore)
        self.geode_cost_in_obsidian = int(geode_cost_in_obsidian)
    
    
    def build_orebot(self, state):
        out = copy.copy(state)
        
        if state["ore"] >= self.ore_cost_in_ore:
            out["ore"] = out["ore"] - self.ore_cost_in_ore
            out["orebots"] = out["orebots"] + 1
            return out
        else:
            print("FAILURE AAHHGHSHGHS ore")
            return None
    
    
    def build_claybot(self, state):
        out = copy.copy(state)
        
        if state["ore"] >= self.clay_cost_in_ore:
            out["ore"] = out["ore"] - self.clay_cost_in_ore
            out["claybots"] = out["claybots"] + 1
            return out
        else:
            print("FAILURE AAHHGHSHGHS clay")
            return None
    
    
    def build_obsidianbot(self, state):
        out = copy.copy(state)
        
        if state["ore"] >= self.obsidian_cost_in_ore and state["clay"] >= self.obsidian_cost_in_clay:
            out["ore"] = out["ore"] - self.obsidian_cost_in_ore
            out["clay"] = out["clay"] - self.obsidian_cost_in_clay
            out["obsidianbots"] = out["obsidianbots"] + 1
            return out
        else:
            print("FAILURE AAHHGHSHGHS obsidian")
            return None
    
    
    def build_geodebot(self, state):
        out = copy.copy(state)
        
        if state["ore"] >= self.geode_cost_in_ore and state["obsidian"] >= self.geode_cost_in_obsidian:
            out["ore"] = out["ore"] - self.geode_cost_in_ore
            out["obsidian"] = out["obsidian"] - self.geode_cost_in_obsidian
            out["geodebots"] = out["geodebots"] + 1
            return out
        else:
            print("FAILURE AAHHGHSHGHS geode")
            return None
        
    def get_build_options(self, state):
        ore = state["ore"]
        clay = state["clay"]
        obsidian = state["obsidian"]
        
        options = {
            "orebots": 0,
            "claybots": 0,
            "obsidianbots": 0,
            "geodebots": 0
        }
        
        if ore >= self.ore_cost_in_ore:
            options["orebots"] = 1
        
        if ore >= self.clay_cost_in_ore:
            options["claybots"] = 1
        
        if ore >= self.obsidian_cost_in_ore and clay >= self.obsidian_cost_in_clay:
            options["obsidianbots"] = 1
        
        if ore >= self.geode_cost_in_ore and obsidian >= self.geode_cost_in_obsidian:
            options["geodebots"] = 1
        
        return options
        
    def __repr__(self):
        return 'Blueprint %d: Each ore robot costs %d ore. Each clay robot costs %d ore. Each obsidian robot costs %d ore and %d clay. Each geode robot costs %d ore and %d obsidian.'%(self._id, self.ore_cost_in_ore, self.clay_cost_in_ore, self.obsidian_cost_in_ore, self.obsidian_cost_in_clay, self.geode_cost_in_ore, self.geode_cost_in_obsidian)


def make_key(state, time_remaining):
    return (state["ore"], state["clay"], state["obsidian"], state["geode"], state["orebots"], state["claybots"], state["obsidianbots"], state["geodebots"], time_remaining)
    
def calculate_best_state(blueprint, state, time_remaining, lookup = {}):
    # print("\n")
    # print("Starting round with %d minutes remaining"%time_remaining)
    # print("Starting state", state)
    
    
    if time_remaining == 0:
        return state
    
    key = make_key(state, time_remaining)
    
    if key in lookup:
        # print("Shortcut", key, lookup[key])
        return lookup[key]
        
    # Get the potential options
    options = blueprint.get_build_options(state)
    # print("Options; ", options)
    
    # Let the robots do their thang
    state['ore'] = state['ore'] + state['orebots']
    state['clay'] = state['clay'] + state['claybots']
    state['obsidian'] = state['obsidian'] + state['obsidianbots']
    state['geode'] = state['geode'] + state['geodebots']
    
    # Check what our best possible state is and bail if we're already out of the running
    # The best possible is if we make a new geode guy on every turn from here out.
    # g + (g+1) + (g+2)
    best_possible = state['geode'] + ()
    
    
    # Do a DFS where we try each option (remember, doing nothing is always one of the options)
    states = []
    if options["geodebots"] > 0:
        state2 = blueprint.build_geodebot(state)
        states.append(state2)
    if options["claybots"] > 0:
        state3 = blueprint.build_claybot(state)
        states.append(state3)
    if options["obsidianbots"] > 0:
        state4 = blueprint.build_obsidianbot(state)
        states.append(state4)
    if options["orebots"] > 0:
        state5 = blueprint.build_orebot(state)
        states.append(state5)
    
    # print("States?", states)
    
    
    best_state = calculate_best_state(blueprint, copy.copy(state), time_remaining - 1)
    for s in states:
        next_state = calculate_best_state(blueprint, s, time_remaining - 1)
        if next_state["geode"] > best_state["geode"]:
            print("\n\n------------------------ NEW BEST at time %d --==========="%time_remaining)
            print(next_state)
            best_state = next_state
    
    # print("Best state: ", best_state)
    
    lookup[key] = best_state
    
    if 'best_overall' not in lookup:
        lookup['best_overall'] = best_state['geode']
    elif lookup['best_overall'] < best_state['geode']:
        lookup['best_overall'] = best_state['geode']
        
    print(lookup['best_overall'])
    
    return best_state


def part1():
    time_limit = 24
    
    initial_state = {
        "ore": 0,
        "clay": 0,
        "obsidian": 0,
        "geode": 0,
        "orebots": 1,
        "claybots": 0,
        "obsidianbots": 0,
        "geodebots": 0
    }
        
    blueprints = []
    
    for line in input:
        b = Blueprint(line)
        print(b)
        blueprints.append(b)
            #
    #
    # for b in blueprints:
    #     print(b)
    #     lookup = {}
    #     state = calculate_best_state(b, copy.copy(initial_state), time_limit, lookup)
    #     print(state)
    
    print(calculate_best_state(blueprints[1], copy.copy(initial_state), time_limit, {}))
    
    return 0
    
    
def part2():
    return 0
    
# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")