# -*- coding: utf-8 -*-
import csv

ofile=open('False_Positive_Study_Donors_reQBT_Format_2.csv', "a")

new_file=open('False_Positive_Study_Donors_reQBT_Format.csv', 'w')
new_file.write("Case Name, C1, C2, C3, C4\n")
with open('Donor_List.csv', 'rb') as file_1:
    reader=csv.reader(file_1)
    donor_list=list(reader)



                    

with open('Donors.csv', 'rb') as file_2:
    reader_2=csv.reader(file_2)
    donors=list(reader_2)


for row in donor_list[1:len(donor_list)]:
    case = row[0]
    for j in range(1, 16):
	new_file.write(case)
        for i in range(1, len(row)):
            list = [] 
            
            if row[i] != "n/a":
                
	        index = donors[0].index(row[i])
                new_file.write(',')
		new_file.write(donors[j][index])
                
                
        new_file.write("\n")
            
