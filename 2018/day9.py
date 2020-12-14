from time import time, strftime, localtime
from datetime import timedelta
from collections import deque

filename = "input9.txt"
# filename = "testinput9.txt"

input = []
with open(filename) as f:
    input = f.readlines()
    # input = [int(x.strip()) for x in input]
    input = [x.strip() for x in input]
    
[players, balls] = [int(x) for x in input[0].split()]
    
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

def playStandard(ball, circle, lastIndex):
    nextInd = (lastIndex + 2) % len(circle)
    if nextInd == 0:
        nextInd = len(circle)
    circle.insert(nextInd, ball)
    return nextInd


def part1():
    start = time()
    print("Part 1")
    print("-"*20)
    
    # Initialize the game
    ballPile = [x for x in range(2, balls+1)]
    circle = [0, 1]
    scores = [0] * players
    cw = True
    
    player = 1 
    lastIndex = 1
    
    while len(ballPile) > 0:
        player += 1
        player = player % players
        if ballPile[0] % 23 == 0:
            # Keep the ball
            ball = ballPile.pop(0)
            scores[player] += ball
            
            # Remove the ball 7 balls ccw
            toRemove = (lastIndex - 7) % len(circle)
            bonusBall = circle.pop(toRemove)
            scores[player] += bonusBall
            lastIndex = toRemove
            pass
        else:
            lastIndex = playStandard(ballPile.pop(0), circle, lastIndex)

    print("\n\nResult: ", max(scores))
    end = time()
    print("Executed in %s seconds"%secondsToStr(end - start))
    
def part2a():
    start = time()
    print("\n\nPart 2")
    print("-"*20)
    
    # players = 9
    # balls = 25
    balls2 = balls * 100
    circle = deque([0])
    scores = [0] * players
    lastIndex = 0
    for ball in range(1, balls2+1):
        if ball % 23 == 0:
            player = ball % players
            circle.rotate(7)
            bonus = circle.pop()
            scores[player] += ball + bonus
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(ball)
        # print (ball, circle)
            # lastIndex = playStandard(ball, circle, lastIndex)
    
    print("\n\nResult: ", max(scores))
    end = time()
    print("Executed in %s seconds"%secondsToStr(end - start))

    
def part2b():
    start = time()
    print("\n\nPart 2")
    print("-"*20)
    balls2 = balls*100
    
    circle = [0, 1]
    scores = [0] * players
    lastIndex = 1
    for ball in range(2, balls2+1):
        if ball % 23 == 0:
            player = ball % players
            toRemove = (lastIndex - 7) % len(circle)
            bonus = circle.pop(toRemove)
            scores[player] += ball + bonus
            lastIndex = toRemove
        else:
            lastIndex = playStandard(ball, circle, lastIndex)
    
    print("\n\nResult: ", max(scores))
    end = time()
    print("Executed in %s seconds"%secondsToStr(end - start))

if __name__ == "__main__":
    part1()
    part2a()
    # part2b()