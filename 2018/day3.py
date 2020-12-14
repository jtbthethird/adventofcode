filename = "input3.txt"
# filename = "testinput3.txt"

input = []
with open(filename) as f:
    input = f.readlines()
    # input = [int(x.strip()) for x in input]
    input = [x.strip() for x in input]
    
#### ---- Begin problem ---- ####
class Entry:
    def __init__(self, row):
        [id, at, start, dims] = row.split()
        self.id = id[1:]
        [self.x, self.y] = start[:-1].split(",")
        [self.width, self.height] = dims.split("x")
        

def part1():
    print("Part 1")
    squares = {}
    for i in input:
        e = Entry(i)
        for xd in range(int(e.x), int(e.x)+int(e.width)):
            for yd in range(int(e.y), int(e.y)+int(e.height)):
                sq = "" + str(xd) + "," + str(yd)
                # print(sq)
                if sq in squares:
                    squares[sq] += 1
                else:
                    squares[sq] = 1
    # print squares
    print(len(filter(lambda z: z > 1, squares.values())))

    
def part2():
    squares = {}
    untouched = []
    for i in input:
        e = Entry(i)
        overlapping = False
        for xd in range(int(e.x), int(e.x)+int(e.width)):
            for yd in range(int(e.y), int(e.y)+int(e.height)):
                sq = "" + str(xd) + "," + str(yd)
                if sq in squares:
                    overlapping = True
                    for otherId in squares[sq]:
                        if otherId in untouched:
                            untouched.remove(otherId)
                else:
                    squares[sq] = [e.id]
        if not overlapping:
            untouched.append(e.id)
    print(untouched)


if __name__ == "__main__":
    part1()
    part2()