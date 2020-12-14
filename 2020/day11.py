import template
import copy
import re

filename="input11.txt"
# filename="testinput11.txt"

input = []
with open(filename) as f:
    input = f.readlines()
    # input = [int(x.strip()) for x in input]
    input = [[z for z in x.strip()] for x in input]
    # input = [[s for s in x] for x in input]

# --- #
# Return True if something changed
def getNewSeat(x, y, data):
    w = data[y][x] 

    minX = max(0, x - 1)
    maxX = min(len(data[0]), x + 1)+1
    minY = max(0, y - 1)
    maxY = min(len(data), y + 1)+1
    
    rows = data[minY:maxY]
    vals = [v for row in rows for v in row[minX:maxX]]
    
    output = w
    if w == 'L':
        # Seat is empty     
        if '#' not in vals:
            output = '#'
        else:
            output = 'L'
    elif w == '#':
        if len([z for z in vals if z == '#']) >= 5:
            output = 'L'
        else:
            output = '#'   
    # print(w, x, y, vals, output)
    return output
    
    
def getFirstSeatVal(x,y,data,d):
    # Dir 0 = right, and proceeds clockwise
    # print("getting seat:", x, y, d)
    seats = []
    iRange = min(len(data), len(data[0]))
    if d == 0:
        seats = [v for v in data[y][x+1:] if v != '.']
    elif d == 1:
        rows = data[y+1:]
        seats = [v for i,row in enumerate(rows) if x+i+1<len(row) for v in row[x+i+1] if v != '.']
    elif d == 2:
        seats = [v for rows in data[y+1:] for v in rows[x] if v != '.']
    elif d == 3:
        rows = data[y+1:]
        seats = [v for i,row in enumerate(rows) if x-i-1>=0 for v in row[x-i-1] if v != '.']
    elif d == 4:
        seats = [v for v in data[y][:x] if v != '.']
        seats.reverse()
    elif d == 5:
        rows = data[:y]
        rows.reverse()
        seats = [v for i,row in enumerate(rows) if x-i-1>=0 for v in row[x-i-1] if v != '.']
    elif d == 6:
        seats = [v for rows in data[:y] for v in rows[x] if v != '.']
        seats.reverse()
    elif d == 7:
        rows = data[:y]
        rows.reverse()
        seats = [v for i,row in enumerate(rows) if x+i+1<len(row) for v in row[x+i+1] if v!= '.']
    # print(seats)
    if len(seats) == 0:
        return 0
    if seats[0] == '#':
        return 1
    return 0
    
def getNewSeat2(x,y,data):
    w = data[y][x]
    
    seats = [getFirstSeatVal(x,y,data,i) for i in range(8)]

    if w == 'L' and sum(seats) == 0:
        return '#'
    
    if w == '#' and sum(seats) >= 5:
        return 'L'
    
    return w
        

def processRound(data, v2=False):
    no_change = True
    c = copy.deepcopy(data)
    output = copy.deepcopy(data)
    for y, row in enumerate(data):
        for x, v in enumerate(row):
            if v in ['L', '#']:
                # Check the surrounding seats
                if v2:
                    s = getNewSeat2(x, y, c)
                else:
                    s = getNewSeat(x, y, c)
                if s != v:
                    output[y][x] = s
                    no_change = False
    return (no_change, output)

def part1():
    # template.printMatrix(input)
    data = copy.copy(input)
    done = False
    while not done:
        (done, data) = processRound(data, False)
        # print(done)
        # template.printMatrix(data)
    # print(data)
    template.printMatrix(data)

    return len([v for row in data for v in row if v == '#'])
    
    # return 0
    
def part2():
    data = copy.copy(input)
    done = False
    
    
    (done, data) = processRound(data, True)
    
    getNewSeat2(3,2,data)
    
    while not done:
        (done, data) = processRound(data, True)
        print(done)
        # template.printMatrix(data)
    print(data)
    template.printMatrix(data)

    return len([v for row in data for v in row if v == '#'])

    

# --- #

if __name__ == "__main__":
    template.funWrapper(part1, "Part 1")
    template.funWrapper(part2, "Part 2")
