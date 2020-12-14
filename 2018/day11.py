from time import time, strftime, localtime
from datetime import timedelta
import math

input = 8444
# input = 42 # Test

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

def cellValue(x, y):
    rackId = x + 10
    power = rackId * y
    power += input
    power = power * rackId
    p = math.floor(power / 100) % 10
    return p - 5

def getInitialTable(size):
    t = [[None for x in range(size)] for y in range(size)]
    for x in range(size):
        for y in range(size):
            t[x][y] = cellValue(x+1,y+1)
    return t


def makeAreaSums(t, size):
    summedAreas = [[None for x in range(size)] for y in range(size)]

    for x in range(size-1, -1, -1):
        for y in range(size-1, -1, -1):
            val = 0
            if x == size-1 and y == size-1:
                summedAreas[x][y] = t[x][y]
            elif x == size-1:
                summedAreas[x][y] = summedAreas[x][y+1] + t[x][y]
            elif y == size-1:
                summedAreas[x][y] = summedAreas[x+1][y] + t[x][y]
            else:
                summedAreas[x][y] =  t[x][y] + summedAreas[x+1][y] + summedAreas[x][y+1] - summedAreas[x+1][y+1]
    return summedAreas


def getNSquareValWithSummedAreas(x, y, n, areaSums):
    size = len(areaSums)
    # print("Getting ", x, y, n, size)
    if x + n == size and y + n == size:
        # print(x,y,n, '---', areaSums[x][y])
        return areaSums[x][y]
    elif y + n == size:
        a = areaSums[x][y]
        b = areaSums[x+n][y]
        out = a - b
        # print(x,y,n, '---',a,b,'=', out)
        return out
    elif x + n == size:
        a = areaSums[x][y]
        b = areaSums[x][y+n]
        out = a - b
        # print(x,y,n, '---',a,b,'=', out)
        return out
    else:
        a = areaSums[x][y]
        b = areaSums[x+n][y]
        c = areaSums[x][y+n]
        d = areaSums[x+n][y+n]
        out = a - b - c + d            
        # print(x,y,n, '---',a,b,c,d,'=', out)
        return out
            

def get33SquareVal(x, y, cache):
    out = 0
    for x1 in range(x, x + 3):
        for y1 in range(y, y + 3):
            cached = cache[y1][x1]
            if cached is not None:
                out += cached
            else:
                res = cellValue(x1+1, y1+1)
                cache[y1][x1] = res
                out += res
    return out

def getNSquareVal(x, y, n, deepCache):
    if n == 0:
        return 0
    out = 0
    # print("Getting: ", x, y, n)
    cachedVal = deepCache[x][y][n-1]
    # print("Cache: ", cachedVal)
    if cachedVal is not None:
        # print("Cache hit: ", x, y, n, cachedVal)
        return cachedVal
    if n == 1:
        val = cellValue(x+1, y+1)
        deepCache[x][y][n-1] = val
        # print("base case", x, y, n, val)
        return val
    elif n % 2 == 0:
        halfN = int(n/2)
        # print("half: ", n, halfN)
        o1 = getNSquareVal(x, y, halfN, deepCache)
        o2 = getNSquareVal(x + halfN, y, halfN, deepCache)
        o3 = getNSquareVal(x, y + halfN, halfN, deepCache)
        o4 = getNSquareVal(x + halfN, y + halfN, halfN, deepCache)
        out = o1 + o2 + o3 + o4
        # print("div 2 case: ", x, y, n, o1, o2, o3, o4, out)
    else:
        # This is an odd num, so we should be able to just do two halves and add a single row
        # halfN = int((n - 1) / 2)
        # print("odd half: ", n, halfN)
        o = getNSquareVal(x, y, n-1, deepCache)
        # o1 = getNSquareVal(x, y, halfN, deepCache)
        # o2 = getNSquareVal(x + halfN, y, halfN, deepCache)
        # o3 = getNSquareVal(x, y + halfN, halfN, deepCache)
        # o4 = getNSquareVal(x + halfN, y + halfN, halfN, deepCache)
        out = o
        # print("odd div 2 case: ", x, y, n, out)
        for x1 in range(n):
            ox = getNSquareVal(x + x1, y + n - 1, 1, deepCache)
            # print("odd div 2 bottom edge: ", x + x1, y+n-1, 1, ox)
            out += ox
        for y1 in range(n - 1):
            oy = getNSquareVal(x + n - 1, y + y1, 1, deepCache)
            # print("odd div 2 side edge: ", x + n -1, y + y1, 1, oy)
            out += oy
        
    deepCache[x][y][n-1] = out
    # print("Got ", x, y, n, "Result: ", out, ".. Cached")
    return out

def part1():
    # Remember, the cellValue 1, 1 is located at 0,0 in this grid
    cache = [[None for x in range(300)] for y in range(300)]
    squares = [[None for x in range(297)] for y in range(297)]
    
    maxVal = float('-inf')
    maxPos = (0,0)
    for y in range(297):
        for x in range(297):
            res = get33SquareVal(x, y, cache)
            squares[y][x] = res
            if res > maxVal:
                maxVal = res
                maxPos = (x+1, y+1)
    
    # prettyPrint2d([x[0:10] for x in cache[0:10]])
                
    return maxPos
    
def part2():
    fullSize = 300
    cache2 = [[[None for z in range(fullSize)] for x in range(fullSize)] for y in range(fullSize)]
    
    maxVal = float('-inf')
    maxPos = (0,0, 0)
    for x in range(fullSize):
        for y in range(fullSize):
            largestSquare = fullSize - max(y,x)
            for n in range(1,largestSquare+1):
                # print("======iterate: ", x,y,n)
                res = getNSquareVal(x, y, n, cache2)
                if res > maxVal:
                    maxVal = res
                    maxPos = (x+1, y+1, n)
                    # print("new max", maxVal, maxPos)
    return maxPos

def part2b():
    size = 300
    initialTable = getInitialTable(size)

    # prettyPrint2d(initialTable)
    
    summedAreas = makeAreaSums(initialTable, size)
    
    # print("-----")
    # prettyPrint2d(summedAreas)
    
    
    maxVal = float('-inf')
    maxPos = (0,0, 0)
    for x in range(size):
        for y in range(size):
            largestSquare = size - max(y,x)
            for n in range(1,largestSquare+1):
                res = getNSquareValWithSummedAreas(x, y, n, summedAreas)
                if res > maxVal:
                    maxVal = res
                    maxPos = (x+1, y+1, n)
                    # print("new max", maxVal, maxPos)
    return maxPos
    
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
    funWrapper(part2b, "Part 2b")
    # funWrapper(part2, "Part 2")