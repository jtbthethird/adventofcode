import template
import copy
import re
import math
import numpy
import plotly.express as px

# filename="input15.txt"
# filename="testinput15.txt"

# input = []
# with open(filename) as f:
#     input = f.readlines()
#     input = [int(x.strip()) for x in input[0].split(',')]
    # input = [[z for z in x.strip()] for x in input]
    # input = [x.strip() for x in input]

input=[0,12,6,13,20,1,17] # Real input
# input=[0,3,6]

# --- #

def part1():
    print(input)
    
    n = 2020
    
    dic = {}

    arr = [input[0]]
    
    for i in range(1,n):
        lastNum = arr[-1]
        diff = None
        if lastNum in dic:
            diff = i - dic[lastNum]
        dic[lastNum] = i
        if i < len(input):
            v = input[i]
            arr.append(input[i])
        elif diff is None:
            arr.append(0)
        else:
            arr.append(diff)
            
        # print(arr)
    
    # print(arr[:10])
    return arr[2019]
    
def part2():
    print(input)
    
    n = 30000000
    
    dic = {}
    
    freq = {}

    arr = [input[0]]
    
    for i in range(1,n):
        lastNum = arr[-1]
        diff = None
        if lastNum in dic:
            diff = i - dic[lastNum]
        dic[lastNum] = i
        if i < len(input):
            v = input[i]
            arr.append(input[i])
        elif diff is None:
            arr.append(0)
        else:
            arr.append(diff)
            
        # print(arr)
    
    # print(arr[:10])
    return arr[n-1]

def ff():
    print(input)
    
    n = 30000000
    # n = 3000000
    
    dic = {}
    
    freq = {}

    arr = [input[0]]
    
    for i in range(1,n):
        lastNum = arr[-1]
        if lastNum not in freq:
            freq[lastNum] = 1
        else:
            freq[lastNum] += 1
        diff = None
        if lastNum in dic:
            diff = i - dic[lastNum]
        dic[lastNum] = i
        if i < len(input):
            v = input[i]
            arr.append(input[i])
        elif diff is None:
            arr.append(0)
        else:
            arr.append(diff)
            
            
    xs = list(freq.keys())
    ys = [freq[k] for k in xs]
    fig = px.scatter(x=xs, y=ys, log_y=True, log_x=True)
    fig.update_xaxes(title_text="Spoken Number")
    fig.update_yaxes(title_text="# of Times Spoken")
    fig.show()
    # print(arr[:20])
    # print(freq)
    # ks = list(freq.keys())
    # print(len(ks))
    # ks.sort()
    # with open("output15.csv", "w") as outFile:
    #     for k in ks:
    #         outFile.write('%d,%d\n'%(k,freq[k]))
    
    # print(arr[:10])
    return arr[n-1]
    

# --- #

if __name__ == "__main__":
    template.funWrapper(part1, "Part 1")
    # template.funWrapper(part2, "Part 2")
    template.funWrapper(ff, "Fun")
