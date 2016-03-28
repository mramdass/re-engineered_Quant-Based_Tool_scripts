# -*- coding: utf-8 -*-
"""
    Munieshwar Ramdass, Eva Revear
    reQBT output file checker for the Validation studies
    20 February 2015
"""

# Notes:
# re.match(r'output.*\.csv$')

import csv, re
from os import walk, path
from random import randint
from math import expm1

RACE = ['BLACK', 'CAUCASIAN', 'HISPANIC', 'ASIAN']
TD = {} # Key: File Name, Data: list of LRs
GENO = {}

def name_files():
    files = []
    for (dirpath, dirnames, filenames) in walk(path.dirname(path.realpath(__file__))):
        files.extend(filenames)
        break
    return files

def read(name):
    numbers = []
    with open(name, 'rb') as f:
        for line in f:
            a_line = line.split(',')
            if len(a_line) == 17:
                genotype_string = a_line[10][1:-1].split(';')
                genotype = (float(genotype_string[0].strip()), float(genotype_string[1].strip()))
                numbers.append((float(a_line[2]), genotype))
    f.close()
    return numbers

def read_csv(name):
    with open(name, 'rb') as f:
        reader = list(csv.reader(f))
    f.close()
    return reader

def generate_combinations(l):
    cl = []
    for i in range(0, len(l)):
        for j in range(i, len(l)):
            cl.append((l[i],l[j]))
    return cl

def generate_genotypes(name):
    alleles = read_csv(name)
    genotypes = {}          # Dictionary of alleles to Dictionary of genotypes
    for i in alleles:
        if i[0] not in genotypes:
            genotypes[i[0]] = []
        genotypes[i[0]].append(float(i[1]))
    for locus in genotypes:
        genotypes[locus] = generate_combinations(genotypes[locus])
    return genotypes

def convert(TD):
    master = {}
    for key in TD:
        sub_keys = key.split('_')
        if sub_keys[2] not in master:                           # Finding case
            master[sub_keys[2]] = {}
        if sub_keys[0] not in master[sub_keys[2]]:              # Finding race
            master[sub_keys[2]][sub_keys[0]] = {}
        if sub_keys[1] not in master[sub_keys[2]][sub_keys[0]]: # Finding Locus
            master[sub_keys[2]][sub_keys[0]][sub_keys[1]] = TD[key]
    return master

def increment(p, a, b, c, d):
    prod = p
    a1 = a
    b1 = b
    e1 = c
    e0 = d
    if prod > 1:
        a1 += 1
    elif prod < 1:
        b1 += 1
    elif prod == 1:
        e1 += 1
    if prod == 0:
        e0 += 1
    return a1, b1, e1, e0

def unique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
        
def unique_alleles(mas):
    observed = []
    for i in mas:
        observed.append(i[1][0])
        observed.append(i[1][1])
    observed = unique(observed)
    observed.remove(-1)
    return observed

def simulate(TD):
    LARGE_INT = expm1(10e+1000)
    GENO = generate_genotypes("Allele_Frequencies.csv")
    master = convert(TD)
    result = {}
    cases_finished = 0
    for case in master:
        if case not in result:
            result[case] = {}
        for race in master[case]:
            if race not in result[case]:
                result[case][race] = {}
            prod = 1
            a1 = 0
            b1 = 0
            e1 = 0
            e0 = 0
            times = 9998
            for i in range(0, times):
                for locus in master[case][race]:
                    #r = randint(0, len(master[case][race][locus]) - 1)
                    r = randint(0, len(GENO[locus]) - 1)
                    rgeno = GENO[locus][r]
                    observed = unique_alleles(master[case][race][locus])
                    if rgeno[0] in observed and rgeno[1] not in observed:
                        for j in range(0, len(master[case][race][locus])):
                            if master[case][race][locus][j][1][0] == rgeno[0] and master[case][race][locus][j][1][1] == float(-1):
                                prod *= master[case][race][locus][j][0]
                                break
                    elif rgeno[0] not in observed and rgeno[1] in observed:
                        for j in range(0, len(master[case][race][locus])):
                            if master[case][race][locus][j][1][0] == rgeno[1] and master[case][race][locus][j][1][1] == float(-1):
                                prod *= master[case][race][locus][j][0]
                                break
                    elif rgeno[0] not in observed and rgeno[1] not in observed:
                        prod *= master[case][race][locus][len(master[case][race][locus]) - 1][0]
                    else:
                        for j in range(0, len(master[case][race][locus])):
                            if rgeno == master[case][race][locus][j][1]:
                                prod *= master[case][race][locus][j][0]
                                break
                a1, b1, e1, e0 = increment(prod, a1, b1, e1, e0)
                prod = 1
            
            for locus in master[case][race]:
                minimum = LARGE_INT
                for i in master[case][race][locus]:
                    if i[0] < minimum:
                        minimum = i[0]
                prod *= minimum
            if 'Min-LR' not in result[case][race]:
                result[case][race]['Min-LR'] = prod
            a1, b1, e1, e0 = increment(prod, a1, b1, e1, e0)
            prod = 1
            for locus in master[case][race]:
                maximum = 0
                for i in master[case][race][locus]:
                    if i[0] > maximum:
                        maximum = i[0]
                prod *= maximum
            if 'Max-LR' not in result[case][race]:
                result[case][race]['Max-LR'] = prod
            a1, b1, e1, e0 = increment(prod, a1, b1, e1, e0)
            prod = 1

            if 'a1' not in result[case][race]:
                result[case][race]['a1'] = float(a1)/(times + 2) * 100
            if 'b1' not in result[case][race]:
                result[case][race]['b1'] = float(b1)/(times + 2) * 100
            if 'e1' not in result[case][race]:
                result[case][race]['e1'] = float(e1)/(times + 2) * 100
            if 'e0' not in result[case][race]:
                result[case][race]['e0'] = float(e0)/(times + 2) * 100
            #print a1, b1, e1, e0
        cases_finished += 1
        print "Cases Finished:", cases_finished
    
    return result

for i in name_files():
    if i.startswith('Evidence_'):
        numbers = read(i)
        if i not in TD:
            sub_names = i.split("_")
            TD[sub_names[2] + "_" + sub_names[3] + "_" + sub_names[4]] = numbers

stats = simulate(TD)
with open("Result.csv", 'w') as f:
    f.write("Case,Race,Above 1,Below 1,Equal 1,Equal 0,Max LR,Min LR\n")
    for i in stats:
        for j in stats[i]:
            f.write(str(i) + ',' + RACE[int(j) - 1] + ',' + str(stats[i][j]['a1']) + ',' + str(stats[i][j]['b1']) + ',' + str(stats[i][j]['e1']) + ',' + str(stats[i][j]['e0']) + ',' + str(stats[i][j]['Max-LR']) + ',' + str(stats[i][j]['Min-LR']) + '\n')
f.close()

