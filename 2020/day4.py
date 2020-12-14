import template
import copy
import re

filename="input4.txt"
# filename="testinput4.txt"

input = []
with open(filename) as f:
    input = f.readlines()
    # input = [int(x.strip()) for x in input]
    input = [x.strip() for x in input]
    # input = [[s for s in x] for x in input]

# ---- #


def part1():
    fieldNames = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]
    currentPP = [0]*len(fieldNames)
    passports = []
    for line in input:
        if line == '':
            passports.append(copy.deepcopy(currentPP))
            currentPP = [0]*len(fieldNames)
            continue
        else:
            fields = line.split(' ')
            for field in fields:
                [fid,val] = field.split(":")
                idx = fieldNames.index(fid)
                # print(idx, "for", fid)
                currentPP[idx] = val

    passports.append(copy.deepcopy(currentPP))
    currentPP = [0]*len(fieldNames)
    
    # print(passports, len(passports))
    
    valids = sum([1 for pp in passports if 0 not in pp[:-1]])
    return valids
    
def part2t():
    hgtre = "(\d+)(cm|in)"
    res = re.match(hgtre, "123in")
    # if res is not None:
    #     print(res.group(2))
        
    hclre = "\#[0-9a-f]{6}"
    res = re.match(hclre, "123abc")
    
    pidre = "^\d{9}$"
    res = re.match(pidre, "0123456789")
    print(res)
    
def part2():
    fieldNames = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]
    currentPP = [0]*len(fieldNames)
    passports = []
    for line in input:
        if line == '':
            passports.append(copy.deepcopy(currentPP))
            currentPP = [0]*len(fieldNames)
            continue
        else:
            fields = line.split(' ')
            for field in fields:
                [fid,val] = field.split(":")
                idx = fieldNames.index(fid)
                # print(idx, "for", fid)
                currentPP[idx] = val

    passports.append(copy.deepcopy(currentPP))
    currentPP = [0]*len(fieldNames)
    
    # print(passports, len(passports))
    
    allfieldspresent = [pp for pp in passports if 0 not in pp[:-1]]
    valids = []
    for pp in allfieldspresent:
        # byr 1920 - 2002
        if int(pp[0]) < 1920 or int(pp[0]) > 2002:
            continue
        
        # iyr 2010 - 2020
        if int(pp[1]) < 2010 or int(pp[1]) > 2020:
            continue
           
        #eyr 2020 - 2030 
        if int(pp[2]) < 2020 or int(pp[2]) > 2030:
            continue
            
        #hgt - cm or in. cm 150-193 in 59-76
        hgtre = "(\d+)(cm|in)"
        res = re.match(hgtre, pp[3])
        if res is None:
            continue
        ht = int(res.group(1))
        if res.group(2) == 'in':
            if ht < 59 or ht > 76:
                continue
        else:
            if ht < 150 or ht > 193:
                continue
                
        # hcl
        hclre = "^\#[0-9a-f]{6}$"
        res = re.match(hclre, pp[4])
        if res is None:
            continue
        
        # ecl
        ecls = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
        if pp[5] not in ecls:
            continue
            
        pidre = "^\d{9}$"
        res = re.match(pidre, pp[6])
        if res is None:
            continue
            
        valids.append(pp)
        
    
    # valids = sum([1 for pp in passports if 0 not in pp[:-1]])
    return len(valids)

if __name__ == "__main__":
    template.funWrapper(part1, "Part 1")
    template.funWrapper(part2, "Part 2")