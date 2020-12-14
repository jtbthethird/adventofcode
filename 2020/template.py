from time import time, strftime, localtime
from datetime import timedelta

filename = "input4.txt"
# filename = "testinput4.txt"

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


def printMatrix(matrix):
    print('\n'.join([''.join([str(cell) for cell in row]) for row in matrix]))
    
    # s = [[str(e) for e in row] for row in matrix]
    # lens = [max(map(len, col)) for col in zip(*s)]
    # fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    # table = [fmt.format(*row) for row in s]
    # print('\n'.join(table))

def getInput(year, day):
    pass

#### ---- Begin problem ---- ####

def part1():
    return 0
    
def part2():
    return 1    
    
    
    
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