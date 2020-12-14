import template
import copy
import re

filename="input7.txt"
# filename="testinput7.txt"

input = []
with open(filename) as f:
    input = f.readlines()
    # input = [int(x.strip()) for x in input]
    input = [x.strip() for x in input]
    # input = [[s for s in x] for x in input]
 
 
# --- #
class BagRule:
    def __init__(self, color):
        self.color = color
        self.contains = []
        self.containedBy = []
        
    def setContainsGold(self):
        self.containsGold = True
        
    def containsColor(self, color):
        for c in self.contains:
            if c[1] == color:
                return True
        return False
        
    def getDeepContainedBy(self, alreadyContainedBy=set()):
        for c in self.containedBy:
            if c.color not in alreadyContainedBy:
                alreadyContainedBy.add(c.color)
                c.getDeepContainedBy(alreadyContainedBy)
        return alreadyContainedBy
        
    def getContainedBags(self):
        myTot = 0
        for rule in self.contains:
            # print(rule)
            sum = rule[0]
            myTot += rule[0] * rule[1].getContainedBags()
        return myTot + 1

def getRules(input):
    allRules = {}
    
    for line in input:
        # First pass, create all the rules, with no children
        # print("\n\nPass 1:", line)
        lineRE = "(?P<outer_bag>[\w ]+) bags contain (?P<inner_bags>.*)"
        out = re.fullmatch(lineRE, line)
    
        outer_color = out.group('outer_bag')
        # print(outer_color)
        if outer_color in allRules:
            print("Duplicate entry!?")
            return -1
        allRules[outer_color] = BagRule(outer_color)
        
    
    for line in input:
        # print("\n\nPass 2:", line)
        lineRE = "(?P<outer_bag>[\w ]+) bags contain (?P<inner_bags>.*)"
        out = re.fullmatch(lineRE, line)
    
        outer_color = out.group('outer_bag')

        inner_bags = out.group('inner_bags')
    
        innerRE = "(?P<num>\d+) (?P<color>[\w ]+) bags?[\.\,]"
        innerBags = re.findall(innerRE, inner_bags)
                
        rule = allRules[outer_color]
        
        contains = [(int(b[0]), allRules[b[1]]) for b in innerBags]
        # print(outer_color, contains)
        rule.contains = contains
        for b in contains:
            b[1].containedBy.append(rule)
    return allRules
    

def part1():

    allRules = getRules(input)

    gold = allRules['shiny gold']
    
    containedBy = gold.getDeepContainedBy()

    # print(containedBy)
    
    return len(containedBy)
        
def part2():
    allRules = getRules(input)

    gold = allRules['shiny gold']
    # print(gold)
    # print(gold.contains)
    
    
    return gold.getContainedBags() - 1
    
    

# --- #

if __name__ == "__main__":
    template.funWrapper(part1, "Part 1")
    template.funWrapper(part2, "Part 2")