# -*- coding: utf-8 -*-
import csv, re
import re
from os import walk, path
 
RACE = ['BLACK', 'CAUCASIAN', 'HISPANIC', 'ASIAN']
race_dict = {'cauc': 'CAUCASIAN', 'black': 'BLACK', 'hisp':'HISPANIC', 'asian': 'ASIAN'};

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
    return LR * .98, LR * .02                 # Equality with 2% error

def getC(file):
	contributors = re.search(r'_C\d', file)
	if contributors:
		C = contributors.group()[1:]
	return C 


def match(f1, f2):
    
    reQBT = read(f1)
    FST = read(f2)
    
    overall_LRs = {};

    i = 0
    while(i < len(reQBT)):
    	j = i - 1
    	race_no = 0
    	if len(reQBT[i]) == 9:
    		while(len(reQBT[j]) != 21):
    			j = j - 1
    		case = reQBT[j][0][:-1]
    		overall_LRs[str(case)] = {};
    		while(len(reQBT[i]) == 9):
    			overall_LRs[str(case)][reQBT[i][2]] = reQBT[i][4];
    			i = i + 1
    			race_no = race_no + 1
    	i = i + 1
    return overall_LRs

def match_FST_LRs(file, dictionary, C, output_file):

	print output_file
	print dictionary
	print '\n'
	LRs = "%s LR" %C
	race = "%s Race" %C

	FST = read(file)
	race_index = FST[0].index(race)
	LR_index = FST[0].index(LRs)
	case_numbers = [row[0] for row in FST]
	first_case = min(dictionary)
	last_case = max(dictionary)
	
	case_races = [row[race_index] for row in FST]
	case_LRs = [row[LR_index] for row in FST]
	
	for i in range(1, len(case_races)):
		
		if 'n/a' not in case_races[i] and str(i) in dictionary:
			
			if '/' in case_races[i]:
				races = case_races[i].split('/')
				print i 
				
				race_1  = race_dict[str(races[0].lower())]
				race_2 = race_dict[str(races[1].lower())]
				print dictionary[str(i)][str(race_1)]
				print dictionary[str(i)][str(race_2)]
				print case_LRs[i]
				with open("Results.csv", "a") as f:
					f.write(str(i)  + ','+ case_races[i] + "," +str(case_LRs[i])+ "," + str(dictionary[str(i)][str(race_1)]) + "," + str(dictionary[str(i)][str(race_2)] + "\n"))
				f.close()
				
			else:
				race_1 = race_dict[case_races[i].lower()]
				print i
				print dictionary[str(i)][str(race_1)]
				print case_LRs[i]
				with open("Results.csv", "a") as f:
					f.write(str(i) + "," + case_races[i] + "," + str(case_LRs[i]) + ","  + str(dictionary[str(i)][str(race_1)]) + "\n")
				f.close()


# MAIN
with open("Results.csv", "w") as f:
    f.write("Case,FST Race,FST LR,reQBT LR  1,reQBT LR 2\n")
for k in name_files():
    if k.startswith('output'):
    	LR_dictionary = match(k, 'FST_LRs.csv')
    	print LR_dictionary
    	for i in range(0, len(LR_dictionary)):
    		for j in range(0, len(RACE)):
    			if str(i) in LR_dictionary:
    				with open("LR_Dictionary.csv", "a") as f:
						f.write(str(i) + "," + RACE[j] + ","  + str(LR_dictionary[str(i)][str(RACE[j])]) + "\n")

    	C = getC(k)
        
    	match_FST_LRs('FST_LRs.csv', LR_dictionary, C, k)

f.close()
