import csv

def read(name):
    matrix = []
    with open(name, 'rb') as f:
        matrix = list(csv.reader(f))
    f.close()
    return matrix

def unique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

with open("Unique.csv", 'w') as f:
    matrix = read("reQBT_False_Positive_Study.csv")
    for i in matrix:
        case = i[0][:-1]
        locus = i[1]
        contr = i[2]
        dec = i[3]
        quant = i[4]
        person = i[5]
        rep1 = i[6]
        rep2 = i[7]
        rep3 = i[8]
        lis = unique(rep1.strip("NEG").strip("INC").split(';') + rep2.strip("NEG").strip("INC").split(';') + rep3.strip("NEG").strip("INC").split(';'))
        if lis[len(lis) - 1] == '':
            lis.pop(len(lis) - 1)
        str_lis = ';'.join(lis)
        f.write(case + "," + locus + "," + contr + "," + dec + "," + quant + "," + person + "," + rep1 + "," + rep2 + "," + rep3 + "," + str_lis + "," + str(len(lis)) + "\n")
    f.close()

with open("Average.csv", 'w') as f:
    matrix = read("Unique.csv")
    matrix.pop(0)
    summation = 0
    index = 0
    for i in matrix:
        index += 1
        summation += int(i[10])
        if index == 15:
            f.write(i[0] + "," + str(summation) + "," + str(summation/float(15)) + "\n")
            summation = 0
            index = 0
    f.close()
