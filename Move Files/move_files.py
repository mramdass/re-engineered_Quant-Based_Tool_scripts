import shutil
import csv, re, json
from os import walk, path
from random import randint, uniform
from math import expm1
 
RACE = ['BLACK', 'CAUCASIAN', 'HISPANIC', 'ASIAN']
LOCUS = ['D8','D21','D7','CSF','D3','TH01','D13','D16','D2','D19','vWA','TPOX','D18','D5','FGA']

#src = "/home/scanner/."
#dst = "/home/Administrator/"
src = "C:/Users/Kevin/Desktop/Casework Script/OLD/"
dst = "C:/Users/Kevin/Desktop/Casework Script/"

#shutil.move(src, dst)

def name_files():
    files = []
    for (dirpath, dirnames, filenames) in walk(path.dirname(path.realpath(__file__))):
        files.extend(filenames)
        break
    return files

for i in name_files():
    if i.startswith('Evidence_'):
        sub_names = i.split("_")
        if int(sub_names[4]) not in [9, 18, 27, 117, 119, 193, 206, 209, 241, 242, 247, 266, 402, 420, 430, 443]:
            shutil.move(src + i, dst)
