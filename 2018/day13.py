from time import time, strftime, localtime
from datetime import timedelta
import copy

filename = "input13.txt"
# filename = "testinput13.txt"

input = []
with open(filename) as f:
    input = f.readlines()
    # input = [int(x.strip()) for x in input]
    input = [x for x in input]

def secondsToStr(elapsed=None):
    if elapsed is None:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())
    else:
        return str(timedelta(seconds=elapsed))


def prettyPrint2d(matrix):
    print('\n'.join([''.join([str(cell) for cell in row]) for row in matrix]))
    
    # s = [[str(e) for e in row] for row in matrix]
    # lens = [max(map(len, col)) for col in zip(*s)]
    # fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    # table = [fmt.format(*row) for row in s]
    # print('\n'.join(table))

#### ---- Begin problem ---- ####
def loadTrack(ins):
    track = [[x for x in row] for row in ins]
    return track

class Cart:
    def __init__(self, id, pos, dir, track):
        self.id = id
        self.pos = pos
        # Dir is a velocity pair, e.g. (0, 1) or (-1, 0)
        # Down is positive!
        self.dir = dir
        # Turns go "left, straight, right" == [0, 1, 2]
        self.nextTurn = 0
        self.track = copy.deepcopy(track)

    def charForCart(self):
        if self.dir == (0, 1):
            return "v"
        if self.dir == (0, -1):
            return "^"
        if self.dir == (1, 0):
            return ">"
        if self.dir == (-1, 0):
            return "<"

    def checkTurn(self, newPos):
        newChar = self.track[newPos[1]][newPos[0]]
        turns = {
            "/": {
                (0, -1): (1, 0),
                (0, 1): (-1, 0),
                (1, 0): (0, -1),
                (-1, 0): (0, 1)
            },
            "\\": {
                (0, -1): (-1, 0),
                (0, 1): (1, 0),
                (1, 0): (0, 1),
                (-1, 0): (0, -1)
            },
            "left": {
                (0, -1): (-1, 0), # up -> left
                (0, 1): (1, 0),   # down -> right
                (1, 0): (0, -1),  # right -> up
                (-1, 0): (0, 1)   # left -> down
            },
            "right": {
                (0, -1): (1, 0), # up -> right
                (0, 1): (-1, 0),   # down -> left
                (1, 0): (0, 1),  # right -> down
                (-1, 0): (0, -1)   # left -> up
            }
        }

        # print(self.id, " now at ", newChar, newPos)
        if newChar in turns:
            newDir = turns[newChar][self.dir]
            # print("Was going ", self.dir, "Now going", newDir)
            self.dir = newDir
        elif newChar == '+':
            if self.nextTurn == 0:
                newDir = turns["left"][self.dir]
                # print("Was going ", self.dir, "Now going", newDir)
                self.dir = newDir
            elif self.nextTurn == 2:
                newDir = turns["right"][self.dir]
                # print("Was going ", self.dir, "Now going", newDir)
                self.dir = newDir
            self.nextTurn = (self.nextTurn + 1)%3
                
        
    def checkCrash(self, otherCart):
        if self.pos == otherCart.pos:
            return self.pos
        
    # Return whether or not we moved successfully
    # return None if we moved successfully
    # Return a location if we crashed (where we crashed)
    def move(self, allCarts, withRemove=False):
        # Move forward
        self.pos = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])
        
        # Turn if necessary
        self.checkTurn(self.pos)
        
        # Check for crashes
        for otherCart in allCarts:
            if otherCart.id == self.id:
                continue
            if self.pos == otherCart.pos:
                if withRemove:
                    return [self.id, otherCart.id]
                else:
                    return self.pos
        return None
    
        
def findCarts(track):
    carts = []
    for y,a in enumerate(track):
        for x,c in enumerate(a):
            if c in ['<', '>', 'v', '^']:
                cart = None
                if c == '<':
                    track[y][x] = '-'
                    cart = Cart(len(carts), (x,y), (-1, 0), track)
                elif c == '>':
                    track[y][x] = '-'
                    cart = Cart(len(carts), (x,y), (1, 0), track)
                elif c == '^':
                    track[y][x] = '|'
                    cart = Cart(len(carts), (x,y), (0, -1), track)
                elif c == 'v':
                    track[y][x] = '|'
                    cart = Cart(len(carts), (x,y), (0, 1), track)
                carts.append(cart)
    return carts


def printTrack(track, carts):
    track2 = copy.deepcopy(track)
    for cart in carts:
        c = cart.charForCart()
        # print(cart.id, c)
        track2[cart.pos[1]][cart.pos[0]] = c
    prettyPrint2d(track2)
    

# --- Main funcs ----

def part1():
    track = loadTrack(input)
    # prettyPrint2d(track)
    
    
    carts = findCarts(track)
    print()

    # printTrack(track, carts)
    
    while True:
        carts = sorted(carts, key=lambda c: (c.pos[1], c.pos[0]))
        for cart in carts:
            # print(cart.id, cart.pos, cart.dir)
            res = cart.move(carts)
            if res is not None:
                # printTrack(track, carts)
                # print("Crash!!!", res)
                return res
    return 0
    
def part2():
    # prettyPrint2d(track)
    track = loadTrack(input)
    
    carts = findCarts(track)
    allCarts = list(carts)

    # printTrack(track, carts)
    
    while True:
        # print("Looping, ", len(carts))
        carts = sorted(carts, key=lambda c: (c.pos[1], c.pos[0]))
        tmp = []
        while len(carts) > 0:
            cart = carts.pop(0)
            tmp.append(cart)
            # print(cart.id, cart.pos, cart.dir)
            ids = cart.move(allCarts, withRemove = True)
            if ids is not None:
                tmp = [t for t in tmp if t.id not in ids]
                carts = [c for c in carts if c.id not in ids]
                allCarts = [c for c in allCarts if c.id not in ids]
        carts = tmp
        # printTrack(track, allCarts)
        if len(carts) == 1:
            # printTrack(track, carts)
            return carts[0].pos
    return 0 
    
    
    
# ---- Wrappers to make things easy/pretty --- #
def funWrapper(fun, name):
    start = time()
    
    result = fun()

    print("\n\n")
    print("-"*20)
    print(name)
    print("-"*20)
    end = time()
    print("Executed in %s seconds"%secondsToStr(end - start))
    print("\n\nResult: ", result)
    

if __name__ == "__main__":
    funWrapper(part1, "Part 1")
    funWrapper(part2, "Part 2")