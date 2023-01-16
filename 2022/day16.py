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

day = "16"

filename="input_"+str(day)+".txt"
# filename="test_"+str(day)+".txt"

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, filename))

input = []

with open(filepath) as f:
    input = [l.strip() for l in f.readlines()] # One entry for each line
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


class Valve:
    def __init__(self, _id, rate, tunnels):
        self._id = _id
        self.rate = rate
        self.tunnels = tunnels
    
    def compute_distance_to_all_nodes(self):
        self.distances = {}
        
        to_compute = [(0, self)]
        
        while to_compute:
            to_compute.sort(key=lambda x: x[0])
                    
            (d, n) = to_compute.pop(0)
            
            if d > 0:
                self.distances[n._id] = d
            
            nexts = [(d + 1, t) for t in n.tunnels]
            
            to_compute = to_compute + nexts
            
            to_compute = [t for t in to_compute if t[1]._id not in self.distances and t[1]._id != self._id]
                        
            
        
    def __repr__(self):
        return "Valve %s has flow rate %d; Leads to %s"%(self._id, self.rate, ", ".join([t._id for t in self.tunnels]))
    
valves = {}

def get_valves():
    global valves
    
    if valves:
        return valves

    for row in input:
        m = re.match(r"Valve (.+) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (([A-Z]+,?[ ]?)+)", row)
    
        (_id, rate, tunnels) = m.groups()[:3]
        tunnels = [t for t in tunnels.split(", ")]
    
        valve = Valve(_id, int(rate), tunnels)
    
        valves[_id] = valve

    for key,val in valves.items():
        new_tunnels = []
        for other_id in val.tunnels:
            new_tunnels.append(valves[other_id])
        val.tunnels = new_tunnels
    

    for v in valves.values():
        v.compute_distance_to_all_nodes()
    
    # print(list(valves.values()))
    
    return valves


def get_best_valve_order(node, valves_on=[], time_remaining=30, prev_release=0, lookup={'best_overall': 0}, debug=False, valves_unavailable=[]):
    if time_remaining == 0:
        print("Hit 0")
        return 0
        
    valves = get_valves()
    
    on_str = ','.join(sorted(valves_on))
    unavail_str = ','.join(sorted(valves_unavailable))
    if debug:
        print("UNavailable: ", valves_unavailable, unavail_str)
        
    # Dynamic programming
    lookup_key = (node._id, on_str, unavail_str, time_remaining)
    if (lookup_key in lookup):
        val = lookup[lookup_key]
        if debug:
            print("Found a match: ", lookup_key, val)
        return val
    
    
    release_per_turn = sum([valves[v].rate for v in valves_on])
    # print("Releasing %d per round"%release_per_turn)
    
    if time_remaining <= 2:
        lookup[lookup_key] = release_per_turn * time_remaining
        return lookup[lookup_key]
    
    # Get all the potential next valves (non-zeros), sort by distance (or value, or expected value)
    # Add them to Q
    
    
    next_valves = [v for v in list(node.distances.keys()) if v not in valves_on and v not in valves_unavailable and valves[v].rate > 0 and node.distances[v] < time_remaining - 1]
    
    # List of ids to visit next
    if debug:
        print("Valves on, unavailable: ", valves_on, valves_unavailable)
        print("Next valves: ", next_valves)
    
    if len(next_valves) == 0:
        # Everything is turned on!
        amount_to_release = release_per_turn * time_remaining
        
        if debug:
            print("Everything is turned on")
            print("releasing %d for %d minutes: %d"%(release_per_turn, time_remaining, amount_to_release))
        
        lookup[lookup_key] = amount_to_release
        return amount_to_release
    
    # We have at least one node still to visit
    # Sort by rate
    next_valves.sort(key=lambda x: valves[x].rate, reverse=True)

    best_result = 0
    
    # For the next item in Q, get the best valve order for it and save the result
    for next_valve in next_valves:
        if debug:
            print("--- Next valve: ", next_valve)
            
        distance = node.distances[next_valve]
        
        added_amount = release_per_turn * (distance + 1)
        tr = time_remaining - node.distances[next_valve] - 1
        
        total = 0
        if tr <= 2:
            if debug:
                print("Under 2 minutes. No time to move and turn something on. Just wait til the 'splosion")
            total = release_per_turn * tr + added_amount
        else:
            if debug:
                print("We've released %d so far. %d minutes remaining. Now recursing..."%(added_amount, tr))
        
            on_2 = copy.copy(valves_on)
            on_2.append(next_valve)
            
            released_so_far = prev_release + added_amount
            
            remaining = get_best_valve_order(valves[next_valve], on_2, tr, released_so_far, lookup, debug, valves_unavailable=valves_unavailable)
        
            total = remaining + added_amount
            # print("Got %d. Plus our previous %d, we end up with %d: "%(remaining, added_amount, total))
        
        if total > best_result:
            if debug:
                print("New BEST!!", total, best_result)
            best_result = total

    if debug:
        print("Best result for ", lookup_key, "is", best_result)
        print("\n--- For reference - size of lookup is", len(lookup.values()))
        print("\n")
    lookup[lookup_key] = best_result
    
    if lookup['best_overall'] < (best_result + prev_release):
        if debug:
            print("New best overall!! ** ", best_result + prev_release)
        lookup['best_overall'] = best_result + prev_release
        
    return best_result


def part1():    
    valves = get_valves()    
    return get_best_valve_order(valves['AA'], debug=False)
    
    
def part2():
    target_valves = [v._id for v in get_valves().values() if v.rate > 0]
    
    start_node = get_valves()['AA']
    
    lookup = {'best_overall': 0}
    
    best_result = 0
    for i in range(math.ceil(len(target_valves)/2)+1):
        my_sets = list(itertools.combinations(target_valves, i))
        for my_set in my_sets:
            # print("\n\n--- New Set---")
            other_set = list(set(target_valves).difference(set(my_set)))
            my_set = list(my_set)
            # print("Getting times for: ", my_set, other_set)
            
            my_time = get_best_valve_order(start_node, valves_on=[], valves_unavailable=other_set, time_remaining=26, debug=False, lookup=lookup)
            other_time = get_best_valve_order(start_node, valves_on=[], valves_unavailable=my_set, time_remaining=26, debug=False, lookup=lookup)
            
            total = my_time + other_time
            # print("Total: ", my_time, other_time, total)
            if total > best_result:
                print("Best Result!", total)
                best_result = total
    
    
    return best_result
    
# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")