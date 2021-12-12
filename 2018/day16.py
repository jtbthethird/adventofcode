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
    
    before_reg = [int(v) for v in sample[0].split(': ')[1][1:-1].split(", ")]
    after_reg = [int(v) for v in sample[2].split(':  ')[1][1:-1].split(", ")]
    args = [int(v) for v in sample[1].split(' ')]
    # print(args)
    
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
        print("Testing opcode: ", op.__name__)
        if reg == after_reg:
            print("MATCH!")
            print("Before: ", before_reg)
            print("Opcode: ", op.__name__)
            print("args: ", args)
            print("After: ", after_reg)
            # print("Match!", op.__name__)
            potential_ops.add(op.__name__)
    
    # print(potential_ops)
    return potential_ops

def part1():
    # print(input[1])
    samples = [sample.split('\n') for sample in input[0].split("\n\n")]
    
    big_samples = 0
    for sample in samples:
        print("\n\nTesting a new sample", sample)
        c = get_potential_opcodes_for_sample(samples[0])
        if len(c) >= 3:
            big_samples += 1
            print("This one counts. Count is at %d"%big_samples)
    
    return big_samples
    
def part2():
    # testprog = input[1].split("\n")
    return 2

# ---- #
    
if __name__ == "__main__":
    template.funWrapper(part1, "Part 1")
    template.funWrapper(part2, "Part 2")