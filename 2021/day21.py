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

day = 21

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
    # input = [list(x) for x in input]
    input = [int(x[-1]) for x in input]

def part1():
    p1 = input[0]
    p2 = input[1]
    
    p1_score = 0
    p2_score = 0
    
    last_roll = 0
    while p1_score < 1000 and p2_score < 1000:
        for i in range(3):
            last_roll = last_roll + 1
            p1 = ((p1 + last_roll - 1) % 10) + 1
        p1_score += p1
        if p1_score >= 1000:
            # print("p1 wins: ", p1_score, last_roll, p2_score)
            return p2_score * last_roll
        for i in range(3):
            last_roll = last_roll + 1
            p2 = ((p2 + last_roll - 1) % 10) + 1
        p2_score += p2
            # p2 += last_roll
        if p2_score > 1000:
            # print("p2 wins: ", p1_score, last_roll, p2_score)
            return p1_score * last_roll
            
        # print("(%d, %d) -> (%d, %d)"%(p1, p2, p1_score, p2_score))
    
    
ways_to_roll = {
    3: 1, # 111
    4: 3, # 112, 121, 211
    5: 6, # 122, 212, 221, 113, 131, 311
    6: 7, # 123, 132, 213, 231, 312, 312, 222
    7: 6, # 322, 232, 223, 331, 313, 133
    8: 3, # 332, 323, 233
    9: 1 # 333
}

""" A dict that's like
        { 
            # From spot 1000, you are done
            1000: { 0: 0}
            # From spot 999, there are 27 ways to get there with 3 rolls
            999: { 3: 27}
            # From spot 998, there are 27 ways to get there with 3 rolls
            998: { 3: 27 }
            # From spot 996:
            # For +3, There is one way to 999 (3 rolls), and from there 27 ways to get from there (with 3 rolls). So 1 * 27 = 27
            # For +4-9, there are 26 ways to get to 1000 with 3 rollsd (sum of 4-9)
            996: { 3: 26, 6: 27 }
            # For 995, there is one way to get to 998, from there 27 ways to get to 1000. So { 6rolls: 27universes }
            #          there are 3 ways to roll a 4 (to 999), from there 27 ways to 1000. So { 6rolls: 81universes }
            #           there are 23 ways left to get to 1000
            995: { 3: 23, 6: 108}
        }
"""
def get_rolls_to_win(from_spot, memo):
    output = {}
    for (k,v) in ways_to_roll.items():
        # print(k, v)
        if from_spot + k >= 21:
            if 3 not in output:
                output[3] = 0
            output[3] += v
        else:
            next_spot = from_spot + k
            next_rolls = memo[next_spot]
            # print("Next roll: ", from_spot, k, next_rolls)
            for nk, nv in next_rolls.items():
                if nk + 3 not in output:
                    output[nk + 3] = 0
                output[nk + 3] += nv * v
    
    memo[from_spot] = output
    
"""
    Ugh.. That's all wrong.
    1. We're only playing to 21
    2. You forgot to take into account the space you're on. You don't just add the score
    
    - 
    It should be something like: On space X, with score Y, how many universes are there for each number of rolls
    So the output should be something like:
    {
        10: {
            20: {  # If I'm on spot 10, and my score is 20, I will win on my next turn in all 27 universes
                1: 27
            }
            19: { 
                1: 27
            },
            ...,
            17: { # If I have 17 points, in one universe, I will roll a 3. Land on spot 3 and end up with 20 points
                    # From there, I'll win on my next turn (27 universes) 1 * get_turns(3, 20) = 27  { 1: 27 }
                    # Otherwise, I'll end up with 21 points (26 remaining universes)
                2: 27
                1: 26
            }
        }
    }
"""
def calc_turns_to_win(from_spot, with_score, target_score, memo):
    # print("---")
    # print("Checking: ", from_spot, with_score)
    score_spot = memo[from_spot][with_score]
    if score_spot != {}:
        return
    for k,v in ways_to_roll.items():
        next_spot = ((from_spot + k - 1) % 10) + 1
        # print("From %d, rolling a %d (%d times) lands on %d"%(from_spot, k, v, next_spot))
        new_score = with_score + next_spot
        if new_score >= target_score:
            if 1 not in score_spot:
                score_spot[1] = 0
            score_spot[1] += v
            # print("Easy win for spot/score (%d,%d) - roll a (%d) %d times. Win with %d points"%(from_spot, with_score, k, v, new_score))
            # print("%d,%d wins %d universes in one roll"%(from_spot, with_score, score_spot[1]))
        else:
            if memo[next_spot][new_score] == {}:
                # print("From (%d,%d), rolled a %d and going deeper to (%d,%d)"%(from_spot, with_score, k, next_spot, new_score))
                calc_turns_to_win(next_spot, new_score, target_score, memo)
            next_info = memo[next_spot][new_score]
            # print("Next spot (%d, %d) results: "%(next_spot, new_score), next_info)
            for nk, nv in next_info.items():
                # print("For spot/score (%d/%d)"%(from_spot, with_score))
                # print("%d turns win %d times: "%(nk+1, nv*v))
                if nk+1 not in score_spot:
                    score_spot[nk + 1] = 0
                score_spot[nk + 1] += v * nv
            # print("... so for (%d,%d) we've updated to: "%(from_spot, with_score), score_spot)
    # print("Final dict for %d,%d"%(from_spot, with_score), score_spot)
    # print("---")
        
        
    
def part2_scratch():
    print(sum(ways_to_roll.values()))
    print(input)
    memo = {}
    for i in range(10):
        memo[i+1] = {}
        for j in range(21):
            memo[i+1][j] = {}
    
    # print(memo)
    
    calc_turns_to_win(input[0], 0, 21, memo)
    calc_turns_to_win(input[1], 0, 21, memo)

    # print(memo) q
    print(memo[input[0]][0])
    print(memo[input[1]][0])
    #
    print(sum(memo[input[0]][0].values()))
    print(sum(memo[input[1]][0].values()))
    print(341960390180808 + 444356092776315)
    p1_wins = 0
    p2_wins = 0
        #
    for p1_turns in sorted(memo[input[0]][0]):
        p1_universes = memo[input[0]][0][p1_turns]
        print("p1", p1_turns, p1_universes )
        for p2_turns, p2_universes in memo[input[1]][0].items():
            # print("p2", p2_turns, p2_universes)
            pass
            
            # if p1 turns 

    print(p1_wins, p2_wins)
    print(444356092776315, 341960390180808)
    
    # print("p1_wins + p2_wins: ", p1_wins + p2_wins)
    # print("Check: ", sum(memo[input[0]][0].values()), sum(memo[input[1]][0].values()), sum(memo[input[0]][0].values()) * sum(memo[input[1]][0].values()))
    
    return 0


def get_wins_for_turn(positions, whos_turn, target_score, memo={}, depth=0, win_tracker=[0,0], multiplier=1):
    # print(depth)
    if (positions, depth) in memo:
        wins = memo[(positions, depth)]
        win_tracker[0] += wins[0] * multiplier
        win_tracker[1] += wins[1] * multiplier
        return (wins, win_tracker)
    # do p1's turn
    wins = [0,0]
    for roll,universes in ways_to_roll.items():
        user_position = positions[whos_turn]
        new_pos = ((user_position[0] + roll - 1) % 10) + 1
        new_score = user_position[1] + new_pos
        # print("Player %d turn (from %d,%d) - Rolled a %d (%d times). Now at %d,%d"%(whos_turn, user_position[0], user_position[1], roll, universes, new_pos, new_score))
        if new_score >= target_score:
            wins[whos_turn] += universes
            # print("Adding %d wins to player %d"%(universes, whos_turn), wins)
            win_tracker[whos_turn] += universes*multiplier
            # print(win_tracker)
        else:
            new_positions = None
            if whos_turn == 0:
                new_positions = ((new_pos, new_score), positions[1])
            else:
                new_positions = (positions[0], (new_pos, new_score))
            [new_wins, t] = get_wins_for_turn(new_positions, (whos_turn + 1)%2, target_score, memo, depth + 1, win_tracker, multiplier*universes)
            # print("Adding %d,%d wins %d times"%(new_wins[0], new_wins[1], universes), wins)
            # print(new_wins)
            wins[0] += universes * new_wins[0]
            wins[1] += universes * new_wins[1]
    # print(wins)
        
    memo[(positions, depth)] = wins
    return (wins, win_tracker)
    
    
    # then do p2's turn
        
def part2():
    p1_pos = (input[0], 0)
    p2_pos = (input[1], 0)

    print(p1_pos, p2_pos)
    
    wins = get_wins_for_turn((p1_pos, p2_pos), 0, 21)
    print(wins)
    
    print(341960390180808 + 444356092776315)
    print(sum(wins[0]))
    print(sum(wins[1]))
    
    return max(wins[1])

    
    

# --- #

if __name__ == "__main__":
    utils.funWrapper(part1, "Part 1")
    utils.funWrapper(part2, "Part 2")