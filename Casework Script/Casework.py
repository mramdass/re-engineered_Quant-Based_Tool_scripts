import csv, re, json
from os import walk, path
from random import randint, uniform
from math import expm1
 
RACE = ['BLACK', 'CAUCASIAN', 'HISPANIC', 'ASIAN']
LOCUS = ['D8','D21','D7','CSF','D3','TH01','D13','D16','D2','D19','vWA','TPOX','D18','D5','FGA']
TD = {}
DONORS = {}
CASE = []
 

def getDonors():
    all_donors_dict = {}
    with open('Donors.csv', 'rb') as file_2:
        reader_2=csv.reader(file_2)
        donors=list(reader_2)
        donor_names = donors[0]
        for i in range(1, len(donor_names)):
            all_donors_dict[donor_names[i]] = {};
            for j in range(1, len(donors)):
                genotype = donors[j][i].split(';')
                allele1 = genotype[0]
                allele2  = genotype[1]
                alleles = (allele1, allele2)
            all_donors_dict[donor_names[i]][donors[j][0]] = alleles

    return all_donors_dict

def name_files():
    files = []
    for (dirpath, dirnames, filenames) in walk(path.dirname(path.realpath(__file__))):
        files.extend(filenames)
        break
    return files

def read(name):
    numbers = {}
    with open(name, 'rb') as f:
        for line in f:
            a_line = line.split(',')
            if len(a_line) == 17:
                key_ = a_line[10][1:-1].split(';')
                key = (key_[0].strip(), key_[1].strip())
                if key not in numbers:
                    numbers[key] = float(a_line[2])
                else:
                    numbers[key] = float(a_line[2])
            elif len(a_line) == 3:
                if a_line[1].startswith('Replicate '):
                    if 'Replicate' not in numbers:
                        alleles = a_line[2].split(';')      # Array of Strings
                        numbers['Replicate'] = alleles
                    else:
                        alleles = a_line[2].split(';')
                        for i in alleles:
                            if i not in numbers['Replicate']:
                                numbers['Replicate'].append(i)

    f.close()
    return numbers
    
def get_LR(donor, name): # name is a tuple (RACE, LOCUS, CASE_NUMBER)
    global TD
    global DONORS
    if name not in TD:
        return 0
    elif 'Replicate' not in TD[name]:
        return 0
    a = donor[0]
    b = donor[1]
    if a not in TD[name]['Replicate']:
        a = '-1'
    if b not in TD[name]['Replicate']:
        b = '-1'
    if a == '-1' and b != '-1':
        temp = a
        a = b
        b = temp
    modified_donor = (a, b)
    return TD[name][modified_donor]

def multiply(l):
    prod = 1
    for i in l:
        prod *= i
    return prod

with open('Donors.csv', 'rb') as file_2:
    reader_2=csv.reader(file_2)
    donors=list(reader_2)
    donor_names = donors[0]
    for i in range(1, len(donor_names)):
        DONORS[donor_names[i]] = {};
        for j in range(1, len(donors)):
            genotype = donors[j][i].split(';')
            allele1 = genotype[0]
            allele2  = genotype[1]
            alleles = (allele1, allele2)
            DONORS[donor_names[i]][donors[j][0]] = alleles

for i in name_files():
    if i.startswith('Evidence_'):
        info = read(i)
        sub_names = i.split("_")
        CASE.append(int(sub_names[4]))
        TD[(sub_names[2], sub_names[3], sub_names[4])] = info

output = {}
for key in DONORS:
    for i in CASE:
        for j in range(1, 5):
            LRS = []
            for k in LOCUS:
                LR = get_LR(DONORS[key][k], (str(j), k, str(i)))
                LRS.append(LR)
            prod = multiply(LRS)
            if key not in output:
                output[key] = {}
                if i not in output[key]:
                    output[key][i] = {}
                    if j not in output[key][i]:
                        output[key][i][j] = prod
                    else:
                        output[key][i][j] = prod
                else:
                    if j not in output[key][i]:
                        output[key][i][j] = prod
                    else:
                        output[key][i][j] = prod
            else:
                if i not in output[key]:
                    output[key][i] = {}
                    if j not in output[key][i]:
                        output[key][i][j] = prod
                    else:
                        output[key][i][j] = prod
                else:
                    if j not in output[key][i]:
                        output[key][i][j] = prod
                    else:
                        output[key][i][j] = prod
            #output[(key, i, j)] = prod
'''
with open('Casework_Results.csv', 'w') as w:
    w.write("Case,Donor,Race,LR\n")
    for i in output:
        d = i[0]
        case = i[1]
        race = i[2]
        w.write(str(case) + ',' + d + ',' + RACE[race - 1] + ',' + str(output[i]) + '\n')
    w.close()
'''
with open('Casework_Results.csv', 'w') as w:
    w.write("Donor,Case,BLACK,CAUCASIAN,HISPANIC,ASIAN,Minumum\n")
    for i in output:#donor
        for j in output[i]:#case
            w.write(str(i) + ',' + str(j) + ',' + str(output[i][j][1]) + ',' + str(output[i][j][2]) + ',' + str(output[i][j][3]) + ',' + str(output[i][j][4]) + ',' + str(min(output[i][j][1], min(output[i][j][2], min(output[i][j][3], output[i][j][4])))) + '\n')
    w.close()
