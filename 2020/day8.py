import template
import copy
import re

filename="input8.txt"
# filename="testinput8.txt"

input = []
with open(filename) as f:
    input = f.readlines()
    # input = [int(x.strip()) for x in input]
    input = [x.strip() for x in input]
    # input = [[s for s in x] for x in input]

# --- #
acc = 0
def parseLine(line):
    print(line)
    lineRE = "(?P<instruction>\w{3}) (?P<sign>\+|\-)(?P<num>\d+)"
    m = re.fullmatch(lineRE, line)
    arg = int(m.group('num'))
    if m.group('sign') == '-':
        arg *= -1
    instr = m.group('instruction')
    # print(instr, arg)
    return(instr, arg)

def part1():
    acc = 0
    visited = set()
    
    i = 0
    while i not in visited:
        visited.add(i)
        (instr, arg) = parseLine(input[i])
        if instr == 'nop':
            i += 1
        elif instr == 'acc':
            acc += arg
            i += 1
        elif instr == 'jmp':
            i += arg
    
    return acc
    

def runLoop(cmds):
    acc = 0
    visited = set()
    lastCmd = len(cmds)
    i = 0
    while i not in visited:
        if i == lastCmd:
            return acc
        visited.add(i)
        (instr, arg) = cmds[i]
        # print(i, instr, arg)
        if instr == 'nop':
            i += 1
        elif instr == 'acc':
            acc += arg
            i += 1
        elif instr == 'jmp':
            i += arg
    
    return None    

def part2():
    cmds = []
    for c in input:
        line = parseLine(c)
        cmds.append(line)
        
    for i, line in enumerate(cmds):
        (inst, arg) = line
        if inst == 'jmp':
            cop = copy.deepcopy(cmds)
            cop[i] = ('nop', arg)
            res = runLoop(cop)
            if res is not None:
                return res
        elif inst == 'nop':
            cop = copy.deepcopy(cmds)
            cop[i] = ('jmp', arg)
            res = runLoop(cop)
            if res is not None:
                return res
    return 1
        
        
    

 # --- #

if __name__ == "__main__":
    template.funWrapper(part1, "Part 1")
    template.funWrapper(part2, "Part 2")