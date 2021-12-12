import template
import copy
import regex as re
import math 
import numpy as np
import plotly.express as px

filename="input21.txt"
# filename="testinput21.txt"

input = []
with open(filename) as f:
    # input = [groups.split('\n') for groups in f.read().split('\n\n')]
    input = f.readlines()
    # input = [int(x.strip()) for x in input[0].split(',')]
    # input = [[z for z in x.strip()] for x in input]
    input = [x.strip() for x in input]
    
# --- #

def part1():
    lines = [line.split(' (contains ') for line in input]
    # print(lines)
    
    all_ingredients = []

    allergy_sets = {}

    known_allergens = set()
    solved_allergies = set()
    
    allergen_to_ing = {}
    
    for food in lines:
        ings = food[0].strip().split(' ')
        all_ingredients += ings
        allgs = food[1][:-1].split(', ')

        print("\nRaw ingredients/allergens")
        print(ings, allgs)
        
        ings = [ing for ing in ings if ing not in known_allergens]
        allgs = [alg for alg in allgs if alg not in solved_allergies]
        
        print("Filtered ings/allgs")
        print(ings, allgs)
        
        for allergy in allgs:
            if allergy in allergy_sets:
                allergy_sets[allergy] = allergy_sets[allergy].intersection(set(ings))
            else:
                allergy_sets[allergy] = set(ings)
            if len(allergy_sets[allergy]) == 1:
                ingred = list(allergy_sets[allergy])[0]
                print("Found a match: ", allergy, ingred)
                allergen_to_ing[allergy] = ingred
                known_allergens.add(ingred)
                solved_allergies.add(allergy)
                allergy_sets.pop(allergy)
    
    print("Allergy sets: ", allergy_sets)
    while len(allergy_sets) > 0:
        a2 = copy.deepcopy(allergy_sets)
        for allergy, pot_ingreds in allergy_sets.items():
            diff = pot_ingreds.difference(known_allergens)
            a2[allergy] = diff
            # print("%s could have been "%allergy, pot_ingreds, "but now is", diff)
            if len(diff) == 1:
                ingred = list(diff)[0]
                print("Found a match: ", allergy, ingred)
                known_allergens.add(ingred)
                solved_allergies.add(allergy)
                allergen_to_ing[allergy] = ingred
                a2.pop(allergy)
        allergy_sets = a2
    
    # print(allergy_sets)
    # print(known_allergens)
    # print(all_ingredients)
    # print(ing_to_allergy)
    
    safe_ingredients = [ing for ing in all_ingredients if ing not in known_allergens]

    print("Part 1: ", len(safe_ingredients))
    
    
    
    print("Part 2: ", ','.join([allergen_to_ing[x] for x in sorted(list(solved_allergies))]))
        
    
def part2():
    
    return 2

# --- #

if __name__ == "__main__":
    template.funWrapper(part1, "Part 1")
    template.funWrapper(part2, "Part 2")

    
        