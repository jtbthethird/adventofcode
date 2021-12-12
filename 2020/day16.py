import template
import copy
import re
import math
import numpy
import plotly.express as px

filename="input16.txt"
# filename="testinput16.txt"

input = []
with open(filename) as f:
    full_input = f.read()
    sections = full_input.split('\n\n')
    # input = [int(x.strip()) for x in input[0].split(',')]
    # input = [[z for z in x.strip()] for x in input]
    input = [x.strip() for x in input]


# --- #
def parse_rules(rules):
    out = {}
    for rule in rules:
        n = rule.split(':')[0]
        rs = rule.split(':')[1].strip().split(' ')
        r1 = rs[0].split('-')
        r2 = rs[2].split('-')
        range1 = range(int(r1[0]), int(r1[1])+1)
        range2 = range(int(r2[0]), int(r2[1])+1)
        # print(range1, range2)
        out[n] = (range1, range2)
    return out


def check_is_valid_num(num, rules):
    for r in rules.values():
        # print("r", r)
        if num in r[0] or num in r[1]:
            # print("VALID", num, r)
            return 0
    # print("NOT VALID", num)
    return num
    

def error_value_of_ticket(ticket, rules):
    return sum([check_is_valid_num(num, rules) for num in ticket])
    

def part1():
    rules = sections[0].split('\n')
    rules = parse_rules(rules)
    # print(rules)
    my_ticket = sections[1].split('\n')[1]
    other_tickets = sections[2].split('\n')[1:]
    
    # print(rules, my_ticket, other_tickets)
    
    bad_nums = []
    for ti in other_tickets:
        nums = [int(x) for x in ti.split(',')]
        # print(nums)
        bad_nums.append(error_value_of_ticket(nums, rules))

    return sum(bad_nums)
    
def part2():
    rules = parse_rules(sections[0].split('\n'))
    # print(rules)
    
    # print(rules)
    my_ticket = [int(x) for x in sections[1].split('\n')[1].split(',')]
    # print(my_ticket)
    other_tickets = sections[2].split('\n')[1:]
    
    # print(rules, my_ticket, other_tickets)
    
    def check_valid_num_bool(num, rules):
        return any([(num in r[0] or num in r[1]) for r in rules.values()])
    
    def is_ticket_valid(ticket, rules):
        return all([check_valid_num_bool(num, rules) for num in ticket])
    
    valid_tix = []
    for ti in other_tickets:
        nums = [int(x) for x in ti.split(',')]
        # print(nums)
        if is_ticket_valid(nums, rules):
            valid_tix.append(nums)
        # if error_value_of_ticket(nums, rules) == 0:
        #     valid_tix.append(nums)
        
    # valid_tix.append(copy.copy(my_ticket))
    # print(len(valid_tix))
   
    # For each index (0 through len(valid_tix[0]))
    #.   For each rule
    #.        If all the values at this index match this rule, 
    #.        This rule gets this index
    
    def check_rule_on_index(rule, i):
        for t in valid_tix:
            # print(t[i], rule)
            if t[i] in rule[0] or t[i] in rule[1]:
                # This rule could apply
                continue
            else:
                return False
        return True
    
    
    ruleMap = {}
    
    indices_to_check = [i for i in range(len(valid_tix[0]))]
    # print(indices_to_check)
    # for index in indices_to_check:
    while len(indices_to_check) > 0:
        index = indices_to_check.pop(0)
        # print("\n---index", index)
        matches = []
        for rname, rule in rules.items():
            # print("CHECKING RULE: ", rname, rule)
            valid = check_rule_on_index(rule, index)
            if valid:
                print("column %d matches rule %s"%(index,rname))
                # ruleMap[i] = rname
                matches.append(rname)
        if len(matches) == 1:
            print("Found a match", index, matches)
            rules.pop(matches[0], None)
            ruleMap[matches[0]] = index
        else:
            indices_to_check.append(index)
            # print("re-adding", index, indices_to_check, matches)
            print("No perfect match", index, matches)
    print(ruleMap)
    
    
                
    acc = 1
    for k in ruleMap.keys():
        if k.startswith('departure'):
            acc *= my_ticket[ruleMap[k]]
            
    return acc
    
    # return sum(bad_nums)
    

# --- #

if __name__ == "__main__":
    # template.funWrapper(part1, "Part 1")
    template.funWrapper(part2, "Part 2")

    
    