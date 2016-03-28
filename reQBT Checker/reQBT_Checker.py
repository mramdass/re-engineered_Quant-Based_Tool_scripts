# -*- coding: utf-8 -*-
import csv
import re

with open('reQBT_False_Positive_Study - Sheet1.csv', 'rb') as file_1:
    reader=csv.reader(file_1)
    cases=list(reader)

patterns=re.compile(r'^\d+|;\d\d|;\d|\.\d|INC|NEG') 

#str = '6;7;8;9.3;10;14'

#matches = re.findall(patterns, str)

#for match in matches:
    #print match

line_num = 1
for case in cases:
    counter = 6
    for i in range(0,3):
        str = re.sub(patterns, '', case[counter])
        if len(str) > 0:
            print 'alarm',':',line_num,':', str
            #print str
            #print line_num
        counter+=1
    line_num+=1
#print cases
