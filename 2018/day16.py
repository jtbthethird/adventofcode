from collections import defaultdict
import template
import copy

filename="input16.txt"
# filename="testinput16.txt"

input = []
with open(filename) as f:
    input = [groups for groups in f.read().split('\n\n\n\n')]
    # input = f.readlines()
    # input = [int(x.strip()) for x in input]
    # input = [x.strip() for x in input]
    # input = [[s for s in x] for x in input]

# ---- #
def addr(a, b, c, data):
    data[c] = data[a] + data[b]

def addi(a, b, c, data):
    data[c] = data[a] + b

def mulr(a, b, c, data):
    data[c] = data[a] * data[b]

def muli(a, b, c, data):
    data[c] = data[a] * b
    
def banr(a, b, c, data):
    data[c] = data[a] & data[b]

def bani(a, b, c, data):
    data[c] = data[a] & b
    
def borr(a, b, c, data):
    data[c] = data[a] | data[b]
    
def bori(a, b, c, data):
    data[c] = data[a] | b
    
def setr(a, b, c, data):
    data[c] = data[a]
    
def seti(a, b, c, data):
    data[c] = a
    
def gtir(a, b, c, data):
    if a > data[b]:
        data[c] = 1
    else: 
        data[c] = 0
        
def gtri(a, b, c, data):
    if data[a] > b:
        data[c] = 1
    else:
        data[c] = 0

def gtrr(a, b, c, data):
    if data[a] > data[b]:
        data[c] = 1
    else:
        data[c] = 0
    
def eqir(a, b, c, data):
    if a == data[b]:
        data[c] = 1
    else:
        data[c] = 0
        
def eqri(a, b, c, data):
    if data[a] == b:
        data[c] = 1
    else:
        data[c] = 0
        
def eqrr(a, b, c, data):
    if data[a] == data[b]:
        data[c] = 1
    else:
        data[c] = 0

def get_potential_opcodes_for_sample(sample):
    # print(args)
    (before_reg, after_reg, args) = sample
    
    op_funs = [
        addr, addi, 
        mulr, muli, 
        banr, bani, 
        borr, bori, 
        setr, seti, 
        gtir, gtri, gtrr, 
        eqir, eqri, eqrr
    ]
    
    potential_ops = set()
    for op in op_funs:
        reg = copy.copy(before_reg)
        op(args[1], args[2], args[3], reg)
        # print(reg, type(reg), after_reg, type(after_reg))
        # print("Testing opcode: ", op.__name__)
        # print(reg, after_reg)
        if reg == after_reg:
            # print("MATCH!")
            # print("Before: ", before_reg)
            # print("Opcode: ", op.__name__)
            # print("args: ", args)
            # print("After: ", after_reg)
            # print("Match!", op.__name__)
            potential_ops.add(op.__name__)
    
    # print(potential_ops)
    return potential_ops

def get_samples():
    out = []
    samples = [sample.split('\n') for sample in input[0].split("\n\n")]
    for sample in samples:
        # print("parsing sample: ", sample)
        before_reg = [int(v) for v in sample[0].split(': ')[1][1:-1].split(", ")]
        after_reg = [int(v) for v in sample[2].split(':  ')[1][1:-1].split(", ")]
        args = [int(v) for v in sample[1].split(' ')]
        out.append((before_reg, after_reg, args))
    return out
    

def get_opcode_map():
    opcode_map = defaultdict(lambda: set([
        addr.__name__, 
        addi.__name__, 
        mulr.__name__,
        muli.__name__, 
        banr.__name__, 
        bani.__name__, 
        borr.__name__, 
        bori.__name__, 
        setr.__name__, 
        seti.__name__, 
        gtir.__name__, 
        gtri.__name__, 
        gtrr.__name__, 
        eqir.__name__, 
        eqri.__name__, 
        eqrr.__name__
    ]))

    samples = get_samples()

    for sample in samples:
        opcode = sample[2][0]
        potentials = get_potential_opcodes_for_sample(sample)
        # print(opcode, potentials)

        opcode_map[opcode] = opcode_map[opcode].intersection(potentials)

    # Run through it and find any that only have one item
    # Add that number to a "To Delete" list
    # Pop X from the "To delete" list
    # Delete X's match from everyone else
    # If that now only has one, add it to the "to delete" list
    # Add X to "deleted list"

    remaining = set(range(0, 16))
    to_delete = set()


    opcode_list = sorted(opcode_map.items(), key=lambda x: len(x[1]))

    to_delete.add(opcode_list[0][0])


    while len(to_delete) > 0:
        # print(remaining, to_delete)
        code_with_single_func = to_delete.pop()
        func_to_del = next(iter(opcode_map[code_with_single_func]))
        # print("\n\n", "Got a lock for", code_with_single_func, func_to_del)
        opcode_map[code_with_single_func] = globals()[func_to_del]

        remaining.remove(code_with_single_func)
    
        for other_code in iter(remaining):
            # print(other_code, opcode_map[other_code])
            if func_to_del in opcode_map[other_code]:
                # print("Removing", func_to_del, "")
                opcode_map[other_code].remove(func_to_del)
                if len(opcode_map[other_code]) == 1:
                    to_delete.add(other_code)


    return opcode_map


def part1():
    samples = get_samples()
    big_samples = 0
    
    for sample in samples:
        # print("\n\nTesting a new sample", sample)
        
        c = get_potential_opcodes_for_sample(sample)
        if len(c) >= 3:
            big_samples += 1
            # print("This one counts. Count is at %d"%big_samples)    
    return big_samples
    
def part2():
    # print(input[1])
    # testprog = input[1].split("\n")
    opcode_map = get_opcode_map()

    register = [0, 0, 0, 0]
    
    instructions = [[int(y) for y in x.split(' ')] for x in input[1].split('\n')]
    
    # print(instructions)
    
    for instr in instructions:
        # print(instr)
        op = opcode_map[instr[0]]
        op(instr[1], instr[2], instr[3], register)
        
    print(register)
    
    return register[0]
    

# ---- #
    
if __name__ == "__main__":
    template.funWrapper(part1, "Part 1")
    template.funWrapper(part2, "Part 2")