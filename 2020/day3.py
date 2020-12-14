from time import time, strftime, localtime
from datetime import timedelta
import functools

filename = "input3.txt"
# filename = "testinput3.txt"

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

def part1():
    pos = (0,0)
    trees = [[c for c in s] for s in input]
    
    height = len(trees)
    width = len(trees[0])
    
    slope = (3, 1)
    
    treeCount = 0
    
    while pos[1] < height - 1:
        newPos = ((pos[0] + slope[0])%width, pos[1] + slope[1])
        # print("checking: ", newPos)
        if trees[newPos[1]][newPos[0]] == "#":
            treeCount += 1
        pos = newPos    
         
    
    return treeCount
    
def part2():
    trees = [[c for c in s] for s in input]
    
    height = len(trees)
    width = len(trees[0])
    
    slopes = [(1, 1), (3, 1), (5, 1), (7,1), (1, 2)]
    
    treeCounts = []
    
    for slope in slopes:
    
        treeCount = 0
        pos = (0,0)

        while pos[1] < height - 1:
            newPos = ((pos[0] + slope[0])%width, pos[1] + slope[1])
            # print("checking: ", newPos)
            if trees[newPos[1]][newPos[0]] == "#":
                treeCount += 1
            pos = newPos    
        treeCounts.append(treeCount)
    
    print(treeCounts)
    out = functools.reduce(lambda a,b: a * b, treeCounts)
    return out 
    
    
    
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