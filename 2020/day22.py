import template
import copy
import regex as re
import math 
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


filename="input22.txt"
# filename="testinput22.txt"

input = []
with open(filename) as f:
    input = [[int(x) for x in groups.split('\n')[1:]] for groups in f.read().split('\n\n')]
    # input = f.readlines()
    # input = [int(x.strip()) for x in input[0].split(',')]
    # input = [[z for z in x.strip()] for x in input]
    # input = [x.strip() for x in input]
    
# --- #

def simulate_round(deck1, deck2):
    d1 = copy.copy(deck1)
    d2 = copy.copy(deck2)
    # print(deck1, deck2)
    c1 = d1.pop(0)
    c2 = d2.pop(0)
    if c1 > c2:
        d1.append(c1)
        d1.append(c2)
    else:
        d2.append(c2)
        d2.append(c1)
    return (d1, d2)

def part1():
    deck1 = copy.copy(input[0])
    deck2 = copy.copy(input[1])
    # simulate_round(input[0], input[1])
    
    deck_lengths = np.array([])
    rounds = np.array([])
    d1_scores = np.array([])
    d2_scores = np.array([])
    i = 0
    while len(deck1) > 0 and len(deck2) > 0:
        i += 1
        # print("Round %d. Fight!"%i)
        deck_lengths = np.append(deck_lengths, len(deck1) - len(deck2))
        d1_scores = np.append(d1_scores, score_deck(deck1))
        d2_scores = np.append(d2_scores, score_deck(deck2))
        rounds = np.append(rounds, i)
        
        (deck1, deck2) = simulate_round(deck1, deck2)
    
    winner = np.array(deck1)
    if len(deck1) == 0:
        print("Player 2 won")
        winner = np.array(deck2)
    else:
        print("Player 1 won")

    # print(scores)
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Scatter(x=rounds, y=deck_lengths, name="Deck Size Difference"), secondary_y=False)
    fig.add_trace(go.Scatter(x=rounds, y=d1_scores, name="Deck 1 Score"), secondary_y=True)
    fig.add_trace(go.Scatter(x=rounds, y=d2_scores, name="Deck 2 Score"), secondary_y=True)
    
    
    fig.show()


    return score_deck(winner)
    
    
def current_state(deck1, deck2):
    return '_'.join([str(c) for c in deck1]) + '|' + '_'.join([str(c) for c in deck2])


def score_deck(winner):
    winner = np.flip(winner)
    scores = np.arange(1, len(winner)+1)
    score = np.dot(scores, winner)
    return score
    
total_rounds = 0
def recursive_combat(deck1, deck2, roundId, gameId):
    global total_rounds
    total_rounds += 1
    d1 = copy.copy(deck1)
    d2 = copy.copy(deck2)
    # print(deck1, deck2)
    c1 = d1.pop(0)
    c2 = d2.pop(0)
    
    if len(d1) < c1 or len(d2) < c2:
        # print("----A player doesn't have enough cards----")
        # print("%d vs %d"%(c1, c2))
        # print(len(d1), c1)
        # print(len(d2), c2)
        if c1 > c2:
            winner = 1
        else:
            winner = 2
    else:
        # Recurse
        (winner, deck) = recursive_combat_game(d1[:c1], d2[:c2], gameId+1)
    # print("Winner of round %d in game %d is Player %d"%(roundId, gameId, winner))
    if winner == 1:
        d1.append(c1)
        d1.append(c2)
    else:
        d2.append(c2)
        d2.append(c1)
    return (d1, d2)


max_depth = 0
def recursive_combat_game(d1, d2, gameId):
    global max_depth
    if gameId > max_depth:
        print("New max: ", gameId)
        max_depth = gameId
    # Return 1 if player 1 wins, return 2 if player 2 wins, plus the winning deck
    # print("="*20)
    # print("=== Starting Game %d ==="%gameId)
    prev_states = set()
    
    deck1 = copy.copy(d1)
    deck2 = copy.copy(d2)
    
    i = 1
    while len(deck1) > 0 and len(deck2) > 0:
        i += 1
        # print("\n----\n==== Round %d (Game %d) ==== Fight!"%(i,gameId))
        # print("The decks are: ")
        # print("Player 1: ", deck1)
        # print("Player 2: ", deck2)
        
        state = current_state(deck1, deck2)
        # print(state)
        if state in prev_states:
            # print("--- Prev state seen in game %d. Player 1 wins---"%gameId)
            return (1, deck1)
        
        prev_states.add(state)
        
        (deck1, deck2) = recursive_combat(deck1, deck2, i, gameId)
        
    
    if len(deck1) == 0:
        # print("Game %d over. Player 2 wins."%gameId)
        return (2, deck2)
    else:
        # print("Game %d over. Player 1 wins."%gameId)
        return (1, deck1)

def part2():
    deck1 = copy.copy(input[0])
    deck2 = copy.copy(input[1])
    
    (winner, deck) = recursive_combat_game(deck1, deck2, 1)
    
    print("GAME OVER...", winner, deck)
    global total_rounds
    print("Total Rounds: ", total_rounds)
    
    return score_deck(deck)

# --- #

if __name__ == "__main__":
    template.funWrapper(part1, "Part 1")
    # template.funWrapper(part2, "Part 2")

    
        