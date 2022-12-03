from time import time, strftime, localtime
from datetime import timedelta

# filename = "input4.txt"
# filename = "testinput4.txt"

# input = []
# with open(filename) as f:
#     input = f.readlines()
#     # input = [int(x.strip()) for x in input]
#     input = [x.strip() for x in input]

def secondsToStr(elapsed=None):
    if elapsed is None:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
    else:
        return str(timedelta(seconds=elapsed))


def printMatrix(matrix, joiner=''):
    print('\n'.join([joiner.join([str(cell) for cell in row]) for row in matrix]))
    
    # s = [[str(e) for e in row] for row in matrix]
    # lens = [max(map(len, col)) for col in zip(*s)]
    # fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    # table = [fmt.format(*row) for row in s]
    # print('\n'.join(table))
    
def make2dArray(x_size, y_size, fill=0):
    return [ [fill]*x_size for i in range(y_size) ]
    
def make3dArray(x_size, y_size, z_size, fill=0):
    return [ [ [fill]*x_size for i in range(y_size) ] for j in range(z_size)]

def getInput(year, day):
    pass
    
def split_list(list, split_on):
    out = []
    tmp = []
    for i in range(len(list)):
        if list[i] == split_on:
            out.append(tmp)
            tmp = []
        else:
            tmp.append(list[i])
    out.append(tmp)
        
    return out

#### ---- Begin problem ---- ####

def part1():
    return 0
    
def part2():
    return 1    
    
    
    
# ---- Wrappers to make things easy/pretty --- #
def funWrapper(fun, name):
    start = time()

    print("-"*20)
    print(name)
    print("-"*20)
    
    result = fun()

    end = time()
    print("Executed in %s seconds"%secondsToStr(end - start))
    print("\n\nResult: ", result)
    print("\n\n")
    

if __name__ == "__main__":
    funWrapper(part1, "Part 1")
    funWrapper(part2, "Part 2")