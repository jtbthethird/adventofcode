from time import time, strftime, localtime
from datetime import timedelta

filename = "input10.txt"
# filename = "testinput10.txt"

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
    print('\n'.join([' '.join([str(cell) for cell in row]) for row in matrix]))
    
    # s = [[str(e) for e in row] for row in matrix]
    # lens = [max(map(len, col)) for col in zip(*s)]
    # fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    # table = [fmt.format(*row) for row in s]
    # print('\n'.join(table))

#### ---- Begin problem ---- ####

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def move(self, x, y):
        self.x += x
        self.y += y
        
class Velocity:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
class Star:
    def __init__(self, point, velocity):
        self.point = point
        self.velocity = velocity
        
    def animate(self):
        self.point.x += self.velocity.x
        self.point.y += self.velocity.y


def printStars(stars, worldX, worldY, prefix=""):
    normalizeStars(stars)
    arr = ['.'] * (worldX+1)
    world = [['.' for x in range(worldX+1)] for y in range(worldY+1)]
    
    for s in stars:
        p = s.point
        world[p.y][p.x] = '#'
    
    print()
    print(prefix)
    prettyPrint2d(world)
    
def normalizeStars(stars):
    minX = min([s.point.x for s in stars])
    minY = min([s.point.y for s in stars])
    
    for s in stars:
        s.point.x -= minX
        s.point.y -= minY
    
    
def worldDims(stars):
    minX = min([s.point.x for s in stars])
    minY = min([s.point.y for s in stars])
    
    maxX = max([s.point.x for s in stars])
    maxY = max([s.point.y for s in stars])
    return (maxX - minX, maxY - minY)

def parseInput():
    stars = []
    
    minX = 0
    minY = 0
    for row in input:
        xPos = int(row[10:row.find(',')])
        yPos = int(row[row.find(',')+1:row.find(">")])
        minX = min(minX, xPos)
        minY = min(minY, yPos)
        
        vel = row.split("velocity=<")[1]
        xVel = int(vel[0:vel.find(",")])
        yVel = int(vel[vel.find(",")+1:vel.find(">")])
        
        point = Point(xPos, yPos)
        velocity = Velocity(xVel, yVel)
        star = Star(point, velocity)
        stars.append(star)
    
    for star in stars:
        star.point.move(-minX, -minY)

    return stars

def part1():
    stars = parseInput()
    
    worldX = max([s.point.x for s in stars])
    worldY = max([s.point.y for s in stars])
    print(worldX, worldY)
    print(worldDims(stars))
    
    # printStars(stars, worldX, worldY, "Initial State")
    
    foundPattern = False
    for i in range(100000):
        for s in stars:
            s.animate()
        dims = worldDims(stars)
        if dims[0] < 100 and dims[1] < 100:
            foundPattern = True
            printStars(stars, dims[0], dims[1], "Seconds: %d"%(i+1))
        if dims[0] > 100 and dims[1] > 100 and foundPattern:
            return 0
            
        
#             if s.point.x < 0 or s.point.x >= worldX or s.point.y < 0 or s.point.y >= worldY:
#                 return -1
#         printStars(stars, worldX, worldY, "Iteration %d"%i)
    return 0
    
def part2():
    return 0 
    
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