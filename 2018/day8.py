filename = "input8.txt"
# filename = "testinput8.txt"

input = []
with open(filename) as f:
    input = f.readlines()
    # input = [int(x.strip()) for x in input]
    input = [x.strip() for x in input]
    
    
def prettyPrint2d(matrix):
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))
    
    # s = [[str(e) for e in row] for row in matrix]
    # lens = [max(map(len, col)) for col in zip(*s)]
    # fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    # table = [fmt.format(*row) for row in s]
    # print('\n'.join(table))

#### ---- Begin problem ---- ####
class Node:
    def __init__(self, data):
        self.numChildren = data.pop(0)
        self.numMetadata = data.pop(0)
        
        self.children = []
        self.metadata = []
        for i in range(0, self.numChildren):
            self.children.append(Node(data))
        
        for i in range(0, self.numMetadata):
            self.metadata.append(data.pop(0))
            
    def sumMetadata(self):
        mySum = sum(self.metadata)
        if self.numChildren == 0:
            return mySum
        
        childSum = sum([c.sumMetadata() for c in self.children])
        return mySum + childSum
        
    def nodeValue(self):
        if self.numChildren == 0:
            return sum(self.metadata)
        
        out = 0
        for i in self.metadata:
            index = i - 1
            if index < len(self.children):
                out += self.children[index].nodeValue()
        return out

def part1():
    print("Part 1\n------")
    data = [int(x.strip()) for x in input[0].split()]
    
    tree = Node(data)
        
    print("\n\nResult: ", tree.sumMetadata())
    
def part2():
    print("\n\nPart 2\n------")
    data = [int(x.strip()) for x in input[0].split()]
    
    tree = Node(data)
    
    print("\n\nResult: ", tree.nodeValue())

if __name__ == "__main__":
    part1()
    part2()