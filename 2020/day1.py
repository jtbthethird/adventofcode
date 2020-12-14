filename = "day1input.txt"

input = []
with open(filename) as f:
    input = f.readlines()
    input = [int(x.strip()) for x in input]
        
#### ---- Begin problem ---- ####

def part1():
    for i, n in enumerate(input):
        for j, m in enumerate(input[i:]):
            if n+m == 2020:
                print(n, m, n*m)
                return
        

    
def part2():
    for i, n in enumerate(input):
        for j, m in enumerate(input[i:]):
            for k, o in enumerate(input[j:]):
                if n+m+o == 2020:
                    print(n, m, k, n*m*o)
                    return


if __name__ == "__main__":
    part1()
    part2()