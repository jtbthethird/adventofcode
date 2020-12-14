from time import time, strftime, localtime
from datetime import timedelta

filename = "input12.txt"
# filename = "testinput12.txt"

initialState = "#.##.###.#.##...##..#..##....#.#.#.#.##....##..#..####..###.####.##.#..#...#..######.#.....#..##...#"
# initialState = "#..#.#..##......###...###"

input = []
with open(filename) as f:
    input = f.readlines()
    # input = [int(x.strip()) for x in input]
    input = [x.strip() for x in input]

def secondsToStr(elapsed=None):
    if elapsed is None:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
    else:
        return str(timedelta(seconds=elapsed))


def prettyPrint2d(matrix):
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))
    
    # s = [[str(e) for e in row] for row in matrix]
    # lens = [max(map(len, col)) for col in zip(*s)]
    # fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    # table = [fmt.format(*row) for row in s]
    # print('\n'.join(table))

#### ---- Begin problem ---- ####

def parseInput():
    rules = {}
    for line in input:
        [a,b] = [x.strip() for x in line.split("=>")]
        rules[a] = b
    # print(rules)
    return rules

def expandState(state):
    newState = list(state)
    prepended = False
    if '#' in state[0:3]:
        prepended = True
        newState.insert(0, '.')
        newState.insert(0, '.')
        newState.insert(0, '.')
    if '#' in state[-3:]:
        newState.append('.')
        newState.append('.')
        newState.append('.')
    return (newState, prepended)
        

def part1():
    prependCount = 0
    state = [c for c in initialState]
    (state, prepended) = expandState(state)
    if prepended:
        prependCount += 3
    rules = parseInput()
    
    iterations = 20
    
    
    for i in range(iterations):
        print(i, ":", ''.join(state))
        new_state = list(state)
        for i in range(2, len(state)-2):
            pots = ''.join(state[i-2:i+3])
            if pots in rules:
                # print("Rule found: ", i, pots, rules[pots])
                new_state[i] = rules[pots]
            else:
                new_state[i] = '.'
        (nstate, prepended) = expandState(new_state)
        state = list(nstate)
        if prepended:
            # print("prepped")
            prependCount += 3
        

    print(20, ":", ''.join(state))
    # for i,p in enumerate(state):
    #     print(i-prependCount,p)
    
    return sum([i-prependCount for (i,p) in enumerate(state) if p == "#"])
    
    
def stateValue(state, offset):
    return sum([i-offset for (i,p) in enumerate(state) if p == "#"])
    

def part2():    
    prependCount = 0
    state = [c for c in initialState]
    (state, prepended) = expandState(state)
    if prepended:
        prependCount += 3
    rules = parseInput()
    
    iterations = 110
    
    print(0, "(%d)"%stateValue(state, prependCount), ":", ''.join(state))
    
    sVal = stateValue(state, prependCount)
    
    for i in range(iterations):
        new_state = list(state)
        for n in range(2, len(state)-2):
            pots = ''.join(state[n-2:n+3])
            if pots in rules:
                # print("Rule found: ", i, pots, rules[pots])
                new_state[n] = rules[pots]
            else:
                new_state[n] = '.'
        (nstate, prepended) = expandState(new_state)
        state = list(nstate)
        if prepended:
            # print("prepped")
            prependCount += 3

        newSVal = stateValue(state, prependCount)
        diff = newSVal - sVal
        sVal = newSVal
        print(i+1, "(%d: %d)"%(sVal, diff), ":", ''.join(state))
        

    
    # for i,p in enumerate(state):
    #     print(i-prependCount,p)
    
    return 6855 + 62*(50000000000-100)

    # return stateValue(state, prependCount)
  
    
    
    
# ---- Wrappers to make things easy/pretty --- #
def funWrapper(fun, name):
    start = time()
    
    result = fun()

    print("-"*20)
    print(name)
    print("-"*20)
    end = time()
    print("Executed in %s seconds"%secondsToStr(end - start))
    print("\n\nResult: ", result)
    print("\n\n")
    

if __name__ == "__main__":
    funWrapper(part1, "Part 1")
    funWrapper(part2, "Part 2")