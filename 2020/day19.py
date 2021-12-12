import template
import copy
import regex as re
import math 
import numpy as np
import plotly.express as px

filename="input19.txt"
# filename="testinput19.txt"

input = []
with open(filename) as f:
    input = [groups.split('\n') for groups in f.read().split('\n\n')]
    # input = f.readlines()
    # input = [int(x.strip()) for x in input[0].split(',')]
    # input = [[z for z in x.strip()] for x in input]
    # input = [x.strip() for x in input]
    
# --- #
def parse_rules(rules):
    rulesdict = {}
    for line in rules:
        (p1,p2) = line.split(":")
        num = p1
        rulesdict[num] = p2.strip()
    return rulesdict    
        
        
def get_re_for_rule(rules, rulenum, processed_rules, part2=False):
    # print("part 2: ", part2)
    if rulenum in processed_rules:
        # print("Got processed rule: ", rulenum, processed_rules[rulenum])
        return processed_rules[rulenum]

    # print("Getting RE for rule: ", rulenum, rules[rulenum])
    rule = copy.copy(rules[rulenum])    
    if rule.startswith('"'):
        # print("Got single letter")
        processed_rules[rulenum] = rule.strip('"')
        return processed_rules[rulenum]
    if rulenum == '8' and part2 is True:
        # print("subbing rule 8")
        newrule = get_re_for_rule(rules, '42', processed_rules, part2)
        newrule = "((%s)+)"%newrule
    elif rulenum == '11' and part2 is True:
        captures = processed_rules['8'].count('(')
        # print("8 captures: ", captures)
        four_two = get_re_for_rule(rules, '42', processed_rules, part2)
        three_one = get_re_for_rule(rules, '31', processed_rules, part2)
        # newrule = r"(%s(?R)?%s)"
        # newrule = r"(\((?R)?\))"
        
        newrule = r"((%s)(?%d)?(%s))"%(four_two, captures+2, three_one)
    else:
        for n in rule.split(' '):
            if n != '|':
                subre = get_re_for_rule(rules, n, processed_rules, part2)
                # print("rule %s"%n, subre)
                re_search_term = r'\b%s\b'%n
                rule = re.sub(re_search_term, "%s"%subre, rule)
        newrule = "(%s)"%rule.replace(' ', '')
    # print("New rule: ",  newrule)
    processed_rules[rulenum] = newrule
    return newrule
        
def regex_from_rules(rules):
    for i in range(len(rules)):
        print(i, get_re_for_rule(rules, str(i)))
    

def part1():
    rules = parse_rules(input[0])
    ruledict = {}
    r = get_re_for_rule(rules, '0', ruledict)
    
    # print("regex", r)
    
    count = 0
    for testcase in input[1]:
        out = re.fullmatch(r, testcase)
        # print(testcase, out)
        if out is not None:
            count += 1
        
    # print("====")
    # print("rule 11: ", ruledict['11'])
    #
    # print("====")
    # print("rule 8: ", ruledict['8'])
    # print("====")
    return count
    
def part2():
    rules = parse_rules(input[0])
    ruledict = {}
    r = get_re_for_rule(rules, '0', ruledict, part2=True)
    # print()
    # print(ruledict)
    # print()
    # print(ruledict['8'])
    # print("\n\neleven", ruledict['11'])
        

    
    # for rulename, ruleval in ruledict.items():
    #     print(rulename, ruleval)
        
    # print('\n\n', r)
    count = 0
    for testcase in input[1]:
        out = re.fullmatch(r, testcase)
        # print(testcase, out)
        if out is not None:
            count += 1
        
    
    return count

# --- #

if __name__ == "__main__":
    template.funWrapper(part1, "Part 1")
    template.funWrapper(part2, "Part 2")

    
    