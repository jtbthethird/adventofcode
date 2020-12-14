import template
import copy
import re
import math

filename="input12.txt"
# filename="testinput12.txt"

input = []
with open(filename) as f:
    input = f.readlines()
    # input = [int(x.strip()) for x in input]
    # input = [[z for z in x.strip()] for x in input]
    input = [x.strip() for x in input]

# --- #
def parseLine(str):
    act = str[0]
    num = int(str[1:])
    return (act, num)

def part1():
    pos = (0,0)
    direction = 0 # East
    
    pi180 = math.pi / 180.0

    for line in input:
        (act, num) = parseLine(line)
        if act == 'F':
            pos = (int(round(pos[0] + (num * math.cos(direction * pi180)))), int(round(pos[1] + (num * math.sin(direction * pi180)))))
        elif act == 'N':
            pos = (pos[0], pos[1] + num)
        elif act == 'S':
            pos = (pos[0], pos[1] - num)
        elif act == 'W':
            pos = (pos[0] - num, pos[1])
        elif act == 'E':
            pos = (pos[0] + num, pos[1])
        elif act == 'R':
            direction = direction - num
        elif act == 'L':
            direction = direction + num
        
    return int(abs(pos[0]) + abs(pos[1]))
    
def part2():
    pos = (0,0)
    waypoint = (10, 1)
        
    for line in input:
        (act, num) = parseLine(line)
        if act == 'F':
            pos = (pos[0] + num * waypoint[0], pos[1] + num * waypoint[1])
            # pos = (int(round(pos[0] + (num * math.cos(direction * pi180)))), int(round(pos[1] + (num * math.sin(direction * pi180)))))
        elif act == 'N':
            waypoint = (waypoint[0], waypoint[1] + num)
        elif act == 'S':
            waypoint = (waypoint[0], waypoint[1] - num)
        elif act == 'W':
            waypoint = (waypoint[0] - num, waypoint[1])
        elif act == 'E':
            waypoint = (waypoint[0] + num, waypoint[1])
        elif num == 180:
            waypoint = (-waypoint[0], -waypoint[1])
        elif act == 'R':
            x, y = waypoint
            xx = x * math.cos(math.radians(num)) + y * math.sin(math.radians(num))
            yy = -x * math.sin(math.radians(num)) + y * math.cos(math.radians(num))
            waypoint = (int(round(xx)), int(round(yy)))
        elif act == 'L':
            x, y = waypoint
            xx = x * math.cos(math.radians(-num)) + y * math.sin(math.radians(-num))
            yy = -x * math.sin(math.radians(-num)) + y * math.cos(math.radians(-num))
            waypoint = (int(round(xx)), int(round(yy)))
    print(pos, waypoint)
        
    return int(abs(pos[0]) + abs(pos[1]))

# --- #

if __name__ == "__main__":
    template.funWrapper(part1, "Part 1")
    template.funWrapper(part2, "Part 2")
