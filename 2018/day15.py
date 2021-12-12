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
        
    def manhattanDistanceTo(self, otherPos):
        return abs(self.x-otherPos.x)+abs(self.y-otherPos.y)

    # BFS Distance to all squares
    # For each adjascent square, store it's position as a key and dist as a value
    # For the 
    def distanceToAllSquares(self, gMap):
        distances = [['#']*len(gMap[0]) for i in range(len(gMap))]
        # Mark the current cell as zero
        distances[self.y][self.x] = 0
        
        # Create a queue of what needs to be checked
        queue = [self]
        while len(queue) > 0:
            spot = queue.pop(0)
            i = distances[spot.y][spot.x]
            spots_to_check = [s for s in spot.adjascentPositions() if s.isAvailable(gMap)]
            # print(spot, i, "spots to check: ", spots_to_check)
            for s in spots_to_check:
                if s not in queue and distances[s.y][s.x] == '#':
                    distances[s.y][s.x] = i+1
                    queue.append(s)
        return distances

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
        self.power = 3
        self.hp = 200
        
    def availableTargets(self, gMap, units):
        # spots = self.pos.adjascentPositions()
        targets = []
        for u in units:
            if u.pos == self.pos:
                continue
            if u.type == self.type:
                continue
            if u.hp <= 0:
                continue
            availables = [s for s in u.pos.adjascentPositions() if s.isAvailable(gMap) and s not in targets]
            targets += availables
        return targets
        
    # Return the target to attack or None
    def selectTarget(self, gMap, units):
        # Sort units
        units_sorted = sorted([u for u in units if u.type != self.type], key=lambda x: (x.hp, x.pos.y, x.pos.x))
        
        adjascents = self.pos.adjascentPositions()
        for u in units_sorted:
            if u.hp <= 0:
                continue
            if u.pos in adjascents:
                return u
        return None

    def move(self, gMap, units):
        if self.hp <= 0:
            return
        # print("Moving: ", self.type, self.pos)
        target_in_range = self.selectTarget(gMap, units)
        if target_in_range is not None:
            # print("In range of a ", target_in_range.type, target_in_range.pos)
            return
        
        availableTargets = self.availableTargets(gMap, units)
        # print("available targets: ", availableTargets)
        if len(availableTargets) == 0:
            return
        distances = self.pos.distanceToAllSquares(gMap)                
        # template.printMatrix(distances)
        targetDistances = [distances[s.y][s.x] for s in availableTargets if distances[s.y][s.x]]
        # print("target distances: ", targetDistances)
        target_dists_for_min = [t for t in targetDistances if t != '#']
        if len(target_dists_for_min) == 0:
            return
        minDist = min(target_dists_for_min)
        nearestTargets = [availableTargets[i] for i,t in enumerate(targetDistances) if t == minDist]
        # print("nearest targets: ", nearestTargets)
        target = sortPosByReadingOrder(nearestTargets)[0]
        # print("Target Spot: ", target)
        distances_to_target = target.distanceToAllSquares(gMap)     
        # template.printMatrix(distances_to_target)
        my_distances = [distances_to_target[s.y][s.x] for s in self.pos.adjascentPositions() if distances_to_target[s.y][s.x] != '#']
        # print("My distances: ", my_distances)
        if len(my_distances) == 0:
            # Nowhere to go!
            return
        min_distance = min(my_distances)
        # print("min dist: ", min_distance)
        first_step = sortPosByReadingOrder([pos for pos in self.pos.adjascentPositions() if distances_to_target[pos.y][pos.x] == min_distance])[0]
        # print("First step: ", first_step)
        gMap[self.pos.y][self.pos.x] = '.'
        self.pos = first_step
        gMap[self.pos.y][self.pos.x] = self.type

    
    def attack(self, gMap, units):
        if self.hp <= 0:
            return
        target = self.selectTarget(gMap, units)
        if target is None:
            return
        # print("Attacking: ", self.type, self.pos)
        # print("In range of a ",target.type, target.pos)
        target.hp -= self.power
        if target.hp <= 0:
            # It DED
            # print(target.type, "at", target.pos, "is DEDD")
            gMap[target.pos.y][target.pos.x] = '.'
        

def sortPosByReadingOrder(positions):
    return sorted(positions, key=lambda pos: (pos.y, pos.x))


def sortUnitsByReadingOrder(units):
    return sorted(units, key=lambda x: (x.pos.y, x.pos.x))
    
    
def combat_is_done(units):
    uTypes = [u.type for u in units if u.hp > 0]
    return 'G' not in uTypes or 'E' not in uTypes
    
    
def printMap(map, units):
    cMap = copy.deepcopy(map)
    print([(u.type, u.pos, u.hp) for u in units])
    for u in units:
        cMap[u.pos.y][u.pos.x] = u.type
    template.printMatrix(cMap)

def simulate_battle(gMap, units):
    i = 0
    printMap(gMap, units)
    while(True):
        units = [u for u in units if u.hp > 0]
        units = sortUnitsByReadingOrder(units)
        
        # if i in [1, 2, 23, 24, 25, 26, 27, 28, 47, 48]:
        # print("After %d rounds"%i)

        # printMap(gMap, units)

        if combat_is_done(units):
            print("Combat is done!")
            break

        for u in units:
            if combat_is_done(units):
                print("Combat is done mid round!")
                print("Combat took %d rounds"%i)
                printMap(gMap, units)
                remaining_health = sum([u.hp for u in units if u.hp > 0])
                return i * remaining_health
            u.move(gMap, units)
            u.attack(gMap, units)
        i = i+1

    print("Combat took %d rounds"%i)
    
    printMap(gMap, units)
    
    remaining_health = sum([u.hp for u in units if u.hp > 0])
    return i * remaining_health

def part1():
    (gMap, units) = loadMap(input)

    printMap(gMap, units)
    
    return simulate_battle(gMap, units)
    
    
def part2():
    # printMap(gMap, units)

    (gMap, units) = loadMap(input)
    starting_elves = len([e for e in units if e.type == 'E'])
    power = 3
    while(True): 
        (gMap, units) = loadMap(input)
        power += 1
        print("\n---\nRunning with power: ", power)
        
        for elf in [u for u in units if u.type == 'E']:
            elf.power = power
    
        result = simulate_battle(gMap, units)
        print("Resulting units: ", [(u.type, u.hp, u.pos) for u in units])
        if len([s.type for s in units if s.hp > 0 and s.type == 'E']) == starting_elves:
            return result
    
if __name__ == "__main__":
    # template.funWrapper(part1, "Part 1")
    template.funWrapper(part2, "Part 2")