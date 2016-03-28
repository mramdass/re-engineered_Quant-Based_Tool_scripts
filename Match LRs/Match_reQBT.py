# -*- coding: utf-8 -*-
import csv, re
import re
from os import walk, path

RACE = ['BLACK', 'CAUCASIAN', 'HISPANIC', 'ASIAN']

def name_files():
    files = []
    for (dirpath, dirnames, filenames) in walk(path.dirname(path.realpath(__file__))):
        files.extend(filenames)
        break
    return files

def read(name):
    matrix = []
    with open(name, 'rb') as f:
        matrix = list(csv.reader(f))
    f.close()
    return matrix

def match(f):
    reQBT = read(f)
    case_map = {}
    f_list = f.split('_')

    for i in range(0, len(reQBT)):
        if len(reQBT[i]) == 9:
            case = -1
            if len(reQBT[i-5]) == 21:           # Getting case name
                case = int(reQBT[i-5][0][:-1])  # Getting rid of the last char
            elif len(reQBT[i-6]) == 21:
                case = int(reQBT[i-6][0][:-1])
            elif len(reQBT[i-7]) == 21:
                case = int(reQBT[i-7][0][:-1])
            
            if case not in case_map:
                case_map[case] = {}
                case_map[case][reQBT[i][2]] = float(reQBT[i][4])
            else:
                case_map[case][reQBT[i][2]] = float(reQBT[i][4])

    with open("Comparison.csv", 'a') as g:
        for i in case_map:
            g.write(str(i) + ',' + str(case_map[i][RACE[0]]) + ',' + str(case_map[i][RACE[1]]) + ',' + str(case_map[i][RACE[2]]) + ',' + str(case_map[i][RACE[3]]) + ',' + f_list[2].strip('.csv') + ',' + str(min(case_map[i][RACE[0]], min(case_map[i][RACE[1]], min(case_map[i][RACE[2]], case_map[i][RACE[3]])))) + '\n')
    g.close()

with open("Comparison.csv", 'w') as f:
    f.write("Case," + RACE[0] + ',' + RACE[1] + ',' + RACE[2] + ',' + RACE[3] + ',Donor Column,Minimum\n')
    for k in name_files():
        if k.startswith('output'):
            match(k)
