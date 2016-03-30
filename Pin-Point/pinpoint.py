import csv, re, json
from os import walk, path
from random import randint, uniform
from math import expm1
 
TD = {}


def read_csv(name):
    with open(name, 'rb') as f:
        reader = list(csv.reader(f))
    f.close()
    return reader

casework = read_csv('Casework_Results.csv')
for i in casework:
    TD[(i[0], i[1])] = i

master = read_csv('Book1.csv')

with open('Matching_the_other_ones.csv', 'w') as f:
    f.write('Case,BLACK,CAUCASIAN,HISPANIC,ASIAN,MINIMUM,,Case,BLACK,CAUCASIAN,HISPANIC,ASIAN,MINIMUM,,Case,BLACK,CAUCASIAN,HISPANIC,ASIAN,MINIMUM,,Case,BLACK,CAUCASIAN,HISPANIC,ASIAN,MINIMUM\n')
    for i in master:
        if i[1] != 'n/a' and (i[1], i[0]) in TD:
            f.write(TD[(i[1], i[0])][1] + ',' + TD[(i[1], i[0])][2] + ',' +TD[(i[1], i[0])][3] + ',' +TD[(i[1], i[0])][4] + ',' +TD[(i[1], i[0])][5] + ',' +TD[(i[1], i[0])][6] +',,')
        if i[2] != 'n/a' and (i[2], i[0]) in TD:
            f.write(TD[(i[2], i[0])][1] + ',' + TD[(i[2], i[0])][2] + ',' +TD[(i[2], i[0])][3] + ',' +TD[(i[2], i[0])][4] + ',' +TD[(i[2], i[0])][5] + ',' +TD[(i[2], i[0])][6] +',,')
        if i[3] != 'n/a' and (i[3], i[0]) in TD:
            f.write(TD[(i[3], i[0])][1] + ',' + TD[(i[3], i[0])][2] + ',' +TD[(i[3], i[0])][3] + ',' +TD[(i[3], i[0])][4] + ',' +TD[(i[3], i[0])][5] + ',' +TD[(i[3], i[0])][6] +',,')
        if i[4] != 'n/a' and (i[4], i[0]) in TD:
            f.write(TD[(i[4], i[0])][1] + ',' + TD[(i[4], i[0])][2] + ',' +TD[(i[4], i[0])][3] + ',' +TD[(i[4], i[0])][4] + ',' +TD[(i[4], i[0])][5] + ',' +TD[(i[4], i[0])][6] +',,')
        f.write('\n')
