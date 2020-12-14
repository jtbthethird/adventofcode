import template
import copy
import re

filename="input5.txt"
# filename="testinput5.txt"

input = []
with open(filename) as f:
    input = f.readlines()
    # input = [int(x.strip()) for x in input]
    input = [x.strip() for x in input]
    # input = [[s for s in x] for x in input]

input = ["BBFFBBFRLL"]
# ---- #


def getSeatId(dirs):
    start = 0
    end = 128
    for d in dirs[:7]:
        size = end - start
        # print(d, size, start, end)
        if d == "F":
            end = start + size/2
        else:
            start = start + size/2
    # print(start, end-1)
    if start != end - 1:
        print("ERROR")
    row = start
    # print("Row: ", row)
    
    start = 0
    end = 8
    for d in dirs[7:]:
        size = end - start
        # print(d, size, start, end)
        if d == "L":
            end = start + size/2
        else:
            start = start + size/2
    col = start
    # print(row, col)
    
    seatId = row*8 + col
    
    # print(seatId)
    
    return int(seatId)
    
    
    
def part1():
    
    maxId = 0
    for row in input:
        dirs = [x for x in row]
    
        maxId = max(maxId, getSeatId(dirs))
        
    for row in input:
        binStr = row.replace("F", '0').replace("B", '1').replace("L", '0').replace("R", '1')
        rowNum = int(binStr, 2)
        print('bin:', rowNum)
    
    return maxId
    
def part2():
    rows = [[x for x in row] for row in input]
    # print(rows)
    seatIds = [getSeatId(dirs) for dirs in rows]
    seatIds.sort()
    # print(seatIds)
    
    seat = [seat for seat in seatIds if (seat + 1) not in seatIds]
    # print(seat)
    return seat[0]+1

# --- #

if __name__ == "__main__":
    template.funWrapper(part1, "Part 1")
    template.funWrapper(part2, "Part 2")