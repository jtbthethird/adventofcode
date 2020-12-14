filename = "input2.txt"

input = []
with open(filename) as f:
    input = f.readlines()
    # input = [int(x.strip()) for x in input]
    input = [x.strip() for x in input]
    
#### ---- Begin problem ---- ####

def part1():
    twos = 0
    threes = 0
    
    for c in input:
        counts = {}
        for x in c:
            if x in counts:
                counts[x] = counts[x] + 1
            else:
                counts[x] = 1
        if 2 in counts.values():
            twos += 1
        if 3 in counts.values():
            threes += 1
    print (twos*threes)
    
    
def part2():
    def diffCount(a, b):
        diffCount = 0
        pos = 0
        for i,x in enumerate(a):
            if x != b[i]:
                diffCount += 1
                pos = i
        if diffCount == 1:
            print("Found!", a, b, pos)
            print(a[:pos] + a[pos+1:])
    
    diffCount("asdfqh", "asgfqh")
    s = input
    s.sort()
    for i,x in enumerate(s):
        for y in s[i:]:
            diffCount(x,y)
    # print(s)


# jbbenqtlavxhivmwyscjukztdp
# jbbenqtlagxhivmwyscjukztdp
# jbbenqtlaxhivmwyscjukztdp
# jbbenqtlaxhivmwyscjukztdp


if __name__ == "__main__":
    part1()
    part2()