import template
import copy
import re
import math
import numpy as np
import plotly.express as px

filename="input17.txt"
# filename="testinput17.txt"

input = []
with open(filename) as f:
    input = f.readlines()
    # input = [int(x.strip()) for x in input[0].split(',')]
    input = [[z for z in x.strip()] for x in input]
    # input = [x.strip() for x in input]

# --- #
def printState(state):
    for l, layer in enumerate(state):
        print("Layer %d"%l)
        template.printMatrix(layer)
        
    

def get_active_neighbors(x,y,z,state):
    lowZ = max(z-1, 0)
    highZ = min(z+2, len(state))
    lowY = max(y-1, 0)
    highY = min(y+2, len(state[0]))
    lowX = max(x-1, 0)
    highX = min(x+2, len(state[0][0]))
    
    acc = 0
    for k in range(lowZ, highZ):
        for j in range(lowY, highY):
            for i in range(lowX, highX):
                if i == x and j == y and k == z:
                    continue
                acc += state[k][j][i]
    return acc
            
            
def add_layers_if_needed(state):
    min_to_add_a_layer = 3
    
    cState = copy.deepcopy(state)
    z0 = sum([v for rows in cState[0] for v in rows])
    if z0 >= min_to_add_a_layer:
        emptyZ = copy.deepcopy([[0]*len(cState[0][0]) for i in range(len(cState[0]))])
        cState.insert(0, emptyZ)
    zMax = sum([v for rows in state[-1] for v in rows])
    if zMax >= min_to_add_a_layer:
        emptyZ = copy.deepcopy([[0]*len(cState[0][0]) for i in range(len(cState[0]))])
        cState.append(emptyZ)

    y0 = sum([v for layer in cState for v in layer[0]])
    if y0 >= min_to_add_a_layer:
        for layer in cState:
            emptyRow = copy.deepcopy([0]*len(cState[0][0]))
            layer.insert(0, emptyRow)
    yMax = sum([v for layer in cState for v in layer[-1]])
    if yMax >= min_to_add_a_layer:
        for layer in cState:
            emptyRow = copy.deepcopy([0]*len(cState[0][0]))
            layer.append(emptyRow)
    
    x0 = sum([row[0] for layer in cState for row in layer])
    if x0 >= min_to_add_a_layer:
        for z in range(len(cState)):
            for y in range(len(cState[0])):
                cState[z][y].insert(0, 0)

    xMax = sum([row[-1] for layer in cState for row in layer])
    if xMax >=  min_to_add_a_layer:
        for layer in cState:
            for row in layer:
                row.append(0)

    return cState
    

def simulateCycle(state):
    state = add_layers_if_needed(state)
    outState = copy.deepcopy(state)
    for z, cols in enumerate(state):
        for y, row in enumerate(cols):
            for x, val in enumerate(row):
                neighbors = get_active_neighbors(x,y,z,state)
                # print(x,y,z,val, neighbors)
                if val == 0 and neighbors == 3:
                    outState[z][y][x] = 1
                elif val == 1 and neighbors in [2,3]:
                    outState[z][y][x] = 1
                else:
                    outState[z][y][x] = 0
    return outState
    
    
def get_active_neighbors_4d(x,y,z,w,state):
    lowW = max(w-1, 0)
    highW = min(w+2, len(state))
    lowZ = max(z-1, 0)
    highZ = min(z+2, len(state[0]))
    lowY = max(y-1, 0)
    highY = min(y+2, len(state[0][0]))
    lowX = max(x-1, 0)
    highX = min(x+2, len(state[0][0][0]))
    
    acc = 0
    
    for m in range(lowW, highW):
        for k in range(lowZ, highZ):
            for j in range(lowY, highY):
                for i in range(lowX, highX):
                    if i == x and j == y and k == z and m == w:
                        continue
                    acc += state[m][k][j][i]
    return acc

            
def add_layers_if_needed_4d(state):
    min_to_add_a_layer = 3
    
    cState = state.copy()
    
    w0 = cState[0].sum()
    # print("woo", w0)
    if w0 >= min_to_add_a_layer:
        world = np.full((cState.shape[1], cState.shape[2], cState.shape[3]),0)
        cState = np.insert(cState, 0, world, axis=0)
    # print(cState)
        
    wMax = cState[-1].sum()
    # print(wMax)
    if wMax >= min_to_add_a_layer:
        world = np.full((cState.shape[1], cState.shape[2], cState.shape[3]),0)
        cState = np.append(cState, [world], axis=0)
    # print(cState)
    
    zSums = cState.sum(axis=0).sum(axis=2).sum(axis=1)
    # print("zsum", zSums)
    z0 = zSums[0]
    zMax = zSums[-1]
    if z0 >= min_to_add_a_layer:
        emptyZ = np.full((cState.shape[2], cState.shape[3]), 0)
        cState = np.insert(cState, 0, emptyZ, axis=1)
        
    # print(cState)
    if zMax >= min_to_add_a_layer:
        emptyZ = np.full((cState.shape[2], cState.shape[3]), 0)
        cState = np.insert(cState, len(cState[0]), emptyZ, axis=1)
    # print(cState)
    
    
    ySums = np.sum(cState, axis=3).sum(axis=1).sum(axis=0)
    y0 = ySums[0]
    if y0 >= min_to_add_a_layer:
        emptyY = np.full((cState.shape[3]), 0)
        cState = np.insert(cState, 0, emptyY, axis=2)

    yMax = ySums[-1]
    if yMax >= min_to_add_a_layer:
        emptyY = np.full((cState.shape[3]), 0)
        cState = np.insert(cState, len(cState[0][0]), emptyY, axis=2)
    
    # print(cState)
    xSums = cState.sum(axis=2).sum(axis=1).sum(axis=0)
    x0 = xSums[0]
    if x0 >= min_to_add_a_layer:
        cState = np.insert(cState, 0, 0, axis=3)
        
    xMax = xSums[-1]
    if x0 >= min_to_add_a_layer:
        cState = np.insert(cState, len(cState[0][0][0]), 0, axis=3)

    return cState
    
def simulate_cycle_4d(state):
    state = add_layers_if_needed_4d(state)
    outState = state.copy()
    for w, world in enumerate(outState):
        for z, cols in enumerate(world):
            for y, row in enumerate(cols):
                for x, val in enumerate(row):
                    neighbors = get_active_neighbors_4d(x,y,z,w,state)
                    if val == 0 and neighbors == 3:
                        outState[w][z][y][x] = 1
                    elif val == 1 and neighbors in [2,3]:
                        outState[w][z][y][x] = 1
                    else:
                        outState[w][z][y][x] = 0
    return outState
    

def part1():
    state = [[0 if v == '.' else 1 for v in row] for row in input]
    print("Initial Value: ")
    template.printMatrix(state)
    print()
    
    state = [state]
    # print(state)
    
    cycles = 6
    
    for i in range(cycles):
        state = simulateCycle(state)
        print("Cycle %d done"%(i+1))
        # printState(state)
    
    return sum([v for layer in state for row in layer for v in row])
    
def part2():
    state = [[0 if v == '.' else 1 for v in row] for row in input]
    nState = np.array([[state]])
    print(nState)
    
    cycles = 6

    for i in range(cycles):
        nState = simulate_cycle_4d(nState)
        print("Cycle %d done"%(i+1))
        # print(nState)
    # print(nState)
    return nState.sum()

def chartState(state, fullX, fullY, fullZ, fullW):
    print("drawing", state.shape)
    


def viz1():
    state = [[0 if v == '.' else 1 for v in row] for row in input]
    print("Initial Value: ")
    template.printMatrix(state)
    print()
    
    state = [state]
    # print(state)
    
    cycles = 6
    
    for i in range(cycles):
        state = simulateCycle(state)
        print("Cycle %d done"%(i+1))
        # printState(state)
        chartState(np.array(state), 20, 20, 20, 1)
    
    return sum([v for layer in state for row in layer for v in row])
    
    
def viz2():
    state = [[0 if v == '.' else 1 for v in row] for row in input]
    nState = np.array([[state]])
    print(nState)
    
    cycles = 6

    for i in range(cycles):
        nState = simulate_cycle_4d(nState)
        print("Cycle %d done"%(i+1))
        chartState(nState, 20, 20, 20, 15)
        # print(nState)
    return nState.sum()
    

# --- #

if __name__ == "__main__":
    template.funWrapper(part1, "Part 1")
    template.funWrapper(viz1, "Visualization 1")
    template.funWrapper(part2, "Part 2")
    template.funWrapper(viz2, "Visualization 2")


    
    