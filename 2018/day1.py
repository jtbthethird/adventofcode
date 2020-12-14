filename = "day1input.txt"
# filename="testinput-day1.txt"

input = []
with open(filename) as f:
    input = f.readlines()
    input = [int(x.strip()) for x in input]
        
#### ---- Begin problem ---- ####

def part1():
    print sum(input)

    
def part2():
    n = 0
    foundVals = {}
    while True:
        print("looping")
        for val in input:
            n = n + val
            if n in foundVals:
                print(n)
                return
            foundVals[n] = True
        


if __name__ == "__main__":
    part1()
    part2()