import os, sys, glob

inFilePath = sys.argv[1]
outFilePath = sys.argv[2]

outFile = open(outFilePath, 'w')
inFile = open(inFilePath)
outFile.write(inFile.readline())

for line in inFile:
    lineItems = line.rstrip().split("\t")
    lineItems[0] = "____".join(lineItems[0].split("____")[:2])
    outFile.write("\t".join(lineItems) + "\n")

inFile.close()
outFile.close()
