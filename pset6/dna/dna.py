from sys import argv, exit
from csv import reader, DictReader



if len(argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    exit(1)

with open(argv[1], 'r') as dna_data:
    dna = reader(dna_data)
    for row in dna:
        dna_file = row
        dna_file.pop(0)
        break

with open(argv[2], 'r') as sequences:
    seq_reader = reader(sequences)
    for row in seq_reader:
        geneline = row
        
dnaline = geneline[0]

genes = {}

for i in dna_file:
    genes[i] = 1

for key in genes:
    l = len(key)
    max = 0
    temp = 0
    for j in range(len(dnaline)):
        while temp > 0:
            temp -= 1
            continue

        if dnaline [j: j + l] == key:
            while dnaline [j - l: j] == dnaline[j: j + l]:
                temp += 1
                j += l

            if temp > max:
                max = temp

    genes[key] +=max

with open(argv[1], newline='') as genefiles:
    genedict = DictReader(genefiles)
    for person in genedict:
        match = 0

        for dnaline in genes:
            if genes[dnaline] == int(person[dnaline]):
                match += 1
        if match == len(genes):
            print(person['name'])
            exit()

    print("No match")


