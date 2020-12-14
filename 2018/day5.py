from string import ascii_lowercase

filename = "input5.txt"
# filename = "testinput5.txt"

input = []
with open(filename) as f:
    input = f.readlines()
    # input = [int(x.strip()) for x in input]
    input = [x.strip() for x in input]
    
#### ---- Begin problem ---- ####

def areEqualAndOppositeCase(a, b):
    if a.lower() == b.lower():
        if a.islower() and b.isupper():
            return True
        if a.isupper() and b.islower():
            return True
    return False


def removePair(str, startingAt=0):
    for i, x in enumerate(str[startingAt:]):
        n = i + startingAt
        if n < len(str) - 1:
            if areEqualAndOppositeCase(x, str[n+1]):
                # print("Removing", n, x, str[n+1])
                # They need to be removed
                str.pop(n)
                str.pop(n)
                # print("removed ", i + startingAt)
                return max(0, n - 1)
    return -1
            
def reducePolymer(arr):
    p = arr
    cont = 0
    while cont >= 0:
        # print(p)
        # print(cont)
        cont = removePair(p, cont)
    out = ''.join(p)
    return(out, len(p))    

def part1():
    print("Part 1")
    p = list(input[0])
    
    (out, len) = reducePolymer(p)
    print(out, len)

    
def part2():
    print("Part 2")
    p = list(input[0])
    lens = []
    for c in ascii_lowercase:
        if c not in p:
            continue
        r = [x for x in p if x != c and x != c.upper()]
        (out, len) = reducePolymer(r)
        lens.append(len)
    print(min(lens))

if __name__ == "__main__":
    part1()
    part2()