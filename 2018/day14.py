from time import time, strftime, localtime
from datetime import timedelta

filename = "input4.txt"
# filename = "testinput4.txt"

input = []
with open(filename) as f:
    input = f.readlines()
    # input = [int(x.strip()) for x in input]
    input = [x.strip() for x in input]
    
input = 380621

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
    # input=2018
    inStr = str(input)
    # arr = [3, 7]
    arr = "37"
    e1 = 0
    e2 = 1
    
    while len(arr) < (input + 10):
        r1 = int(arr[e1])
        r2 = int(arr[e2])
    #
        arr += str(r1 + r2)
        
        e1 = (e1 + (1 + r1))%(len(arr))
        e2 = (e2 + (1 + r2))%(len(arr))
        # print(' '.join(['(%s)'%s if i==i1 else '[%s]'%s if i==i2 else str(s) for i, s in enumerate(arr)]))
    
    return ''.join([str(s) for s in arr][input:input+10])
    
def part2():
    # input= "51589"

    inStr = str(input)
    # arr = [3, 7]
    arr = "37"
    e1 = 0
    e2 = 1
        
    while inStr not in arr[-(len(inStr)+2):]:
        r1 = int(arr[e1])
        r2 = int(arr[e2])
    #
        arr += str(r1 + r2)
        
        e1 = (e1 + (1 + r1))%(len(arr))
        e2 = (e2 + (1 + r2))%(len(arr))
    #
        # indices = [i1, i2]
        # print(' '.join(['(%s)'%s if i==i1 else '[%s]'%s if i==i2 else str(s) for i, s in enumerate(arr)]))
    print(arr.index(inStr))
    return (arr.index(inStr))
    
    
    
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