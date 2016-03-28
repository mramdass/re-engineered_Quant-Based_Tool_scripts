# -*- coding: utf-8 -*-
"""
    Munieshwar Ramdass
    reQBT output file checker for the Validation studies
    20 February 2015
"""

import csv, re
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

def approx(LR):
    return LR * 0.98, LR * 1.02                 # Equality with 2% error

def check(case, race, c, case_map, LR_map):
    if approx(LR_map[case][c])[0] < case_map[case][race] and approx(LR_map[case][c])[1] > case_map[case][race]:
        #print str(case) + ": FST " + c + ", reQBT " + race
        with open("Results.csv", "a") as f:
            f.write(str(case) + ",," + c + "," +str(LR_map[case][c]) + ",," + race + "," + str(case_map[case][race]) + "\n")
        f.close()
    
def match(f1, f2):
    reQBT = read(f1)
    FST = read(f2)
    case_map = {}
    LR_map = {}

    for i in range(0, len(reQBT)):
        if len(reQBT[i]) == 9:
            case = -1
            if len(reQBT[i-5]) == 21:           # Getting case name
                case = int(reQBT[i-5][0][:-1])  # Geeting rid of the last char
            elif len(reQBT[i-6]) == 21:
                case = int(reQBT[i-6][0][:-1])
            elif len(reQBT[i-7]) == 21:
                case = int(reQBT[i-7][0][:-1])
            
            if case not in case_map:
                case_map[case] = {}
                case_map[case][reQBT[i][2]] = float(reQBT[i][4])
            else:
                case_map[case][reQBT[i][2]] = float(reQBT[i][4])

    for i in range(0, len(FST)):
        if FST[i][0] != 'Case':                 # Ignore first line
            if int(FST[i][0]) not in LR_map:
                LR_map[int(FST[i][0])] = {}
                for j in range(1, 5):           # range of C columns 0 to 4
                    if FST[i][j] != 'n/a':
                        LR_map[int(FST[i][0])]['C' + str(j)] = float(FST[i][j])
                    else:
                        LR_map[int(FST[i][0])]['C' + str(j)] = -1.0

    for case in case_map:
        for i in RACE:
            for j in range(1, 5):
                check(case, i, 'C' + str(j), case_map, LR_map)

# MAIN
with open("Results.csv", "w") as f:
    f.write("Case,,FST Column,FST LR,,reQBT Race,reQBT LR\n")
for i in name_files():
    if i.startswith('output'):
        match(i, 'FST_LRs.csv')
f.close()


# Notes:
# re.match(r'output.*\.csv$')
"""
reQBT output format for case_map:
{
    127:
    {
        'HISPANIC':     39769.1,
        'BLACK':        11947.8,
        'CAUCASIAN':    314846.0,
        'ASIAN':        1472210.0
    }
}

FST LR Sheet format for LR_map:
{
    480:
    {
        'C3': '2.62E+01',
        'C2': '1.01E-09',
        'C1': '5.40E-01',
        'C4': '2.70E+04'
    }
}
"""
