import os, sys

inFilePath = sys.argv[1]
colIndex = int(sys.argv[2])
hasHeader = sys.argv[3] == "True"

inFile = open(inFilePath)

if hasHeader:
    inFile.readline()

values = set()
for line in inFile:
    lineItems = line.rstrip("\n").split("\t")
    values.add(lineItems[colIndex])

print(len(values))
