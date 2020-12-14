import template
import copy

filename="input15.txt"
filename="testinput15.txt"
input = []
with open(filename) as f:
    input = f.readlines()
    # input = [int(x.strip()) for x in input]
    input = [x.strip() for x in input]
    input = [[s for s in x] for x in input]

# ---- #
def loadMap(input):
    units = []
    gMap = copy.deepcopy(input)
    for y,r in enumerate(gMap):
        for x,c in enumerate(r):
            if c in ['G', 'E']:
                u = Unit(c, Position(x, y))
                units.append(u)
    return (gMap, units)
    
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def itemAtPos(self, gMap):
        return gMap[self.y][self.x]
        
    def isAvailable(self, gMap):
        return gMap[self.y][self.x] == '.'
        
    #-- Is there a path between this point and the other point
    # -- if so return the distance (because it's a BFS, it's as soon as we find it)
    def travelDistance(self, otherPos, gMap, checked):
        # print("seeing if %s can reach %s"%(self, otherPos), checked)
        if self == otherPos:
            # print("Found a path")
            return 0
        spots_to_check = [s for s in self.adjascentPositions() if s.isAvailable(gMap) and s not in checked]
        for s in spots_to_check:
            checked.add(s)
        # print(checked)
        for s in spots_to_check:
            isReachable = s.travelDistance(otherPos, gMap, checked)
            if isReachable is not None:
                return isReachable + 1
        return None
        
    
    # Return a list of positions from self to the other position
    # If there are multiple shortest paths, return the one where the first step comes first in reading order
    def shortestPathsTo(self, otherPos):
        pass
        
    def adjascentPositions(self):
        spots = [
            Position(self.x, self.y-1),
            Position(self.x-1, self.y),
            Position(self.x+1, self.y),
            Position(self.x, self.y+1)
        ]
        return spots
        
    def __repr__(self):
        return "(%d, %d)"%(self.x, self.y)
        
    def __eq__(self, obj):
        return isinstance(obj, Position) and self.x == obj.x and self.y == obj.y
        
    def __lt__(self, other):
        return self.y < other.y or self.x < other.x
    
    def __hash__(self):
        return hash(repr(self))

class Unit:
    def __init__(self, type, pos):
        self.type = type
        self.pos = pos
        
    def availableTargets(self, gMap, units):
        # spots = self.pos.adjascentPositions()
        targets = []
        for u in units:
            if u.pos == self.pos:
                continue
            availables = [s for s in u.pos.adjascentPositions() if s.isAvailable(gMap) and s not in targets]
            targets += availables
        return targets
        
    def move(self, gMap, units):
        targetSpots = self.availableTargets(gMap, units)
        availableTargets = self.availableTargets(gMap, units)
        targetDistances = [self.pos.travelDistance(s, gMap, set()) for s in availableTargets]
        minDist = min([t for t in targetDistances if t is not None])        
        nearestTargets = [availableTargets[i] for i,t in enumerate(targetDistances) if t == minDist]
        target = sortPosByReadingOrder(nearestTargets)[0]
        
        

def sortPosByReadingOrder(positions):
    return sorted(positions, key=lambda pos: (pos.y, pos.x))

def sortUnitsByReadingOrder(units):
    return sorted(units, key=lambda x: (x.pos.y, x.pos.x))

def part1():
    (gMap, units) = loadMap(input)
    template.printMatrix(gMap)

    elf = sortUnitsByReadingOrder(units)[0]
    print(elf.type)
    
    elf.move(gMap, units)
    
    return 0
    
def part2():
    return 1

if __name__ == "__main__":
    template.funWrapper(part1, "Part 1")
    template.funWrapper(part2, "Part 2")