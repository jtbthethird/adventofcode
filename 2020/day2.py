filename = "input2.txt"
# filename = "testinput2.txt"

input = []
with open(filename) as f:
    input = f.readlines()
    # input = [int(x.strip()) for x in input]
    input = [x.strip() for x in input]
    
#### ---- Begin problem ---- ####

def checkRow(str):
    s = str.split()
    [minV, maxV] = s[0].split('-')
    l = s[1][0]
    p = s[-1]
    
    t = [x for x in p if x == l]
    # print(minV, maxV, l, p)
    return len(t) >= int(minV) and len(t) <= int(maxV)

def part1():
    print("Part 1")
    n = 0
    for i in input:
        x = checkRow(i)
        if x:
            n += 1
        # print(checkRow(i))
        
    out = [1 for i in input if checkRow(i)]
    print(n)
        

def checkRow2(str):
    s = str.split()
    [minV, maxV] = s[0].split('-')
    l = s[1][0]
    p = s[-1]
    # print(minV, maxV, l, p)
    
    a = p[int(minV) - 1] == l
    b = p[int(maxV) - 1] == l
    return (not a and b) or (a and not b)
    
def part2():
    print("Part 2")
    n = 0
    for i in input:
        x = checkRow2(i)
        if x:
            n += 1
    print(n)
    

if __name__ == "__main__":
    part1()
    part2()