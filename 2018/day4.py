filename = "input4.txt"
# filename = "testinput4.txt"

input = []
with open(filename) as f:
    input = f.readlines()
    # input = [int(x.strip()) for x in input]
    input = [x.strip() for x in input]
    
#### ---- Begin problem ---- ####

class SleepRecord:
    def __init__(self, guardId, date, asleepStart, asleepEnd):
        self.guardId = int(guardId)
        self.date = date
        self.asleepStart = asleepStart
        self.asleepEnd = asleepEnd
        self.asleepTime =  asleepEnd - asleepStart
        # print(guardId, date, asleepStart, asleepEnd, self.asleepTime)

class Guard:
    def __init__(self, guardId):
        self.guardId = guardId
        self.sleepTime = 0
        self.sleepMinutes = {}
    
    def addRecord(self, sleepRecord):
        self.sleepTime += sleepRecord.asleepTime
        for x in range(sleepRecord.asleepStart, sleepRecord.asleepEnd):
            if x in self.sleepMinutes:
                self.sleepMinutes[x] += 1
            else:
                self.sleepMinutes[x] = 1

def getDate(row):
    return row[6:11]
    
def getTime(row):
    return int(row[15:17])
    
def processInput():
    input.sort()
    
    entries = []
    
    currentGuard = 0
    asleepTime = 0
    for i in input:
        if i.endswith("begins shift"):
            vals = i.split()
            guard = vals[3]
            currentGuard = guard[1:]
            # print("Guard: ", currentGuard)
        elif i.endswith("asleep"):
            asleepDate = getDate(i)
            asleepTime = getTime(i)
            # print("asleep: ", asleepDate, asleepStart)
        elif i.endswith("wakes up"):
            asleepDate = getDate(i)
            wakeup = getTime(i)
            e = SleepRecord(currentGuard, asleepDate, asleepTime, wakeup)
            entries.append(e)
    return entries
    

def part1():
    print("Part 1")
    sleepEntries = processInput()
    
    guards = {}
    for e in sleepEntries:
        if not e.guardId in guards:
            guards[e.guardId] = Guard(e.guardId)
        guards[e.guardId].addRecord(e)

    sleepyGuards = sorted(guards.values(), key=lambda g: g.sleepTime, reverse=True)
    sleepiestGuard = sleepyGuards[0]
    
    sortedMins = sorted(sleepiestGuard.sleepMinutes.keys(), key=lambda m: sleepiestGuard.sleepMinutes[m], reverse=True)
    print(sortedMins[0] * sleepiestGuard.guardId)
    
    
        
        
    
def part2():
    print("Part 2")
    sleepEntries = processInput()
    
    guards = {}
    for e in sleepEntries:
        if not e.guardId in guards:
            guards[e.guardId] = Guard(e.guardId)
        guards[e.guardId].addRecord(e)

    gId = 0
    maxMins = 0
    minNum = 0
    for g in guards.values():
        sortedMins = sorted(g.sleepMinutes.keys(), key=lambda m: g.sleepMinutes[m], reverse=True)
        sleeps = g.sleepMinutes[sortedMins[0]]
        if sleeps > maxMins:
            gId = g.guardId
            minNum = sortedMins[0]
            maxMins = g.sleepMinutes[minNum]
            print(gId, minNum, maxMins)
    print(gId * minNum)

if __name__ == "__main__":
    part1()
    part2()