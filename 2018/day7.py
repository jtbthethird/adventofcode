filename = "input7.txt"
# filename = "testinput7.txt"

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
class Instruction:
    def __init__(self, letter):
        self.letter = letter
        self.time = ord(letter) - 4 # Make this 4 for prod
        self.parents = []
        self.children = []
        
    def is_available(self, processed):
        out = False
        if len(self.parents) == 0:
            return True
        for p in [p.letter for p in self.parents]:
            if p not in processed:
                return False
        return True
    
    def print_tree(self):
        print([p.letter for p in self.parents], "-> ", self.letter, "->", [c.letter for c in self.children])
        for c in self.children:
            c.print_tree()
            
    def process(self):
        # print("PRocessing ", self.letter)
        self.time = self.time - 1
        if self.time == 0:
            return True
        return False

def loadTree():
    nodes = {}
    for i in input:
        s = i.split()
        l1 = s[1]
        l2 = s[7]
        n1 = None
        n2 = None
        if l1 in nodes:
            n1 = nodes[l1]
        else:
            n1 = Instruction(l1)
            nodes[l1] = n1
        if l2 in nodes:
            n2 = nodes[l2]
        else:
            n2 = Instruction(l2)
            nodes[l2] = n2
            
        n1.children.append(n2)
        n2.parents.append(n1)
    return nodes
    
def part1():
    print("Part 1\n------")
    nodes = loadTree()
    
    # start = [n for n in nodes.values() if len(n.parents) == 0][0]
    # print(start.letter, [c.letter for c in start.children])
    # start.print_tree()
    
    remainingNodes = sorted(list(nodes.values()), key=lambda x: x.letter)
    processed = []
    while len(remainingNodes) > 0:
        # print("Processed: ", processed)
        # print("Looping", [r.letter for r in remainingNodes])
        
        # Take the next item up
        i = -1
        for j, n in enumerate(remainingNodes):
            if n.is_available(processed):
                i = j
                break
        
        # Process the node
        node = remainingNodes.pop(i)

        processed.append(node.letter)        #
        #
        # for c in node.children:
        #     if c not in remainingNodes:
        #         remainingNodes.append(c)

        # Clean up the list
        # remainingNodes = sorted(remainingNodes, key=lambda x: x.letter)
    
    print("\nResult: ", ''.join(processed))
    
def part2():
    print("\n\nPart 2\n------")
    nodes = loadTree()
    
    remainingNodes = sorted(list(nodes.values()), key=lambda x: x.letter)
    availableNodes = []
    processing = []
    processed = []
    
    streams = 5
    
    # for node in remainingNodes:
    #     print(node.letter, node.time, [p.letter for p in node.parents], [c.letter for c in node.children])
    
    secs = 0
    while len(processed) < len(nodes.keys()):
        for n in remainingNodes:
            if n.is_available(processed) and n not in availableNodes and n.letter not in processed:
                availableNodes.append(n)
                remainingNodes.remove(n)

        availableNodes = sorted(availableNodes, key=lambda x: x.letter)
        # print("Available:", [n.letter for n in availableNodes])
        while len(processing) < streams and len(availableNodes) > 0:
            ntp = availableNodes.pop(0)
            processing.append(ntp)
        
        # print("Processing: ", [n.letter for n in processing])
        # print("", secs, [n.letter for n in processing], processed, [x.letter for x in availableNodes])
        completed = []
        for n in processing:
            if n.process():
                # print("Completed ", n.letter)
                completed.append(n)
                
        for n in completed:
            processing.remove(n)
            processed.append(n.letter)
        # print("Processed: ", processed)
    
        secs += 1
        
    
    print("\nResult: ", ''.join(processed), secs)

if __name__ == "__main__":
    part1()
    part2()