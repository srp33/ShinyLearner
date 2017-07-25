import os, sys

inFilePath = sys.argv[1]
outFilePath = sys.argv[2]

inFile = open(inFilePath)
outFile = open(outFilePath, "w")

headerItems = inFile.readline().rstrip("\n").split("\t")
headerItems.insert(1, "Iteration")
outFile.write("\t".join(headerItems) + "\n")

for line in inFile:
    lineItems = line.rstrip("\n").split("\t")
    descriptionItems = lineItems[0].split("____")
    lineItems.insert(1, descriptionItems[1])
    lineItems[0] = descriptionItems[0]

    outFile.write("\t".join(lineItems) + "\n")

outFile.close()
inFile.close()
