import string 

filename = "/Users/jtburgess/Development/advent/2018/input6.txt"
# filename = "/Users/jtburgess/Development/advent/2018/testinput6.txt"

input = []
with open(filename) as f:
    input = f.readlines()
    # input = [int(x.strip()) for x in input]
    input = [x.strip() for x in input]
    
    
def prettyPrint2d(matrix):
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))
    
    # s = [[str(e) for e in row] for row in matrix]
    # lens = [max(map(len, col)) for col in zip(*s)]
    # fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    # table = [fmt.format(*row) for row in s]
    # print('\n'.join(table))
    
#### ---- Begin problem ---- ####

def distToPoint(c1, c2):
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])

def part1():
    print("Part 1\n------")
    
    coords = [(int(x.split(',')[0]), int(x.split(',')[1])) for x in input]
    
    print(coords)
    
    # Find max X and Y
    maxX = sorted(coords, key=lambda c: c[0], reverse=True)[0][0]
    maxY = sorted(coords, key=lambda c: c[1], reverse=True)[0][1]
    
    counts = {}
    letters = {}
    for i, c in enumerate(coords):
        counts[c] = 0
        if i <= 25:
            letters[c] = string.ascii_lowercase[i]
        else:
            letters[c] = string.ascii_lowercase[i % 26] + str(i)
    
    map = []
    excludes = []

    for y in range(0, maxY+1):
        map.append([])
        for x in range(0, maxX+1):
            if (x, y) in coords:
                map[y].append(letters[coord].upper())
                continue
            minDist = maxX + maxY + 2
            coord = None
            for c in coords:
                d = distToPoint(c, (x, y))
                if d == minDist:
                    coord = None
                elif d < minDist:
                    minDist = d
                    coord = c
            if coord != None:
                # print(x, y, "goes to", letters[coord])
                counts[coord] += 1
                map[y].append(letters[coord])
                if x == 0 or y == 0 or x == maxX or y == maxY:
                    if coord not in excludes:
                        excludes.append(coord)
            else:
                map[y].append('.')
                # print(x, y, "goes to", "none")
    # prettyPrint2d(map)
    
    # Remove the infinite values
    validCounts = [counts[v] + 1 for v in counts.keys() if v not in excludes]
    
    print(validCounts)
    
    print(max(validCounts))
    
    
    
def part2():
    print("\n\nPart 2\n------")
    mDist = 10000
    # mDist = 32
    
    coords = [(int(x.split(',')[0]), int(x.split(',')[1])) for x in input]
    
    maxX = sorted(coords, key=lambda c: c[0], reverse=True)[0][0]
    maxY = sorted(coords, key=lambda c: c[1], reverse=True)[0][1]
    
    numSpaces = 0
    for y in range(0, maxY+1):
        for x in range(0, maxX+1):
            # if (x, y) in coords:
            #     continue
            totalD = 0
            for c in coords:
                d = distToPoint(c, (x, y))
                totalD += d
            if totalD < mDist:
                numSpaces += 1
                # print(x, y, "is safe")
    print("\nResult: ", numSpaces)
            

if __name__ == "__main__":
    part1()
    part2()