import os, sys

inFilePath = sys.argv[1]
iterationOutputHeader = sys.argv[2]
outFilePath = sys.argv[3]

outFile = open(outFilePath, 'w')
inFile = open(inFilePath)

headerItems = inFile.readline().rstrip().split("\t")
headerItems.insert(1, "Inner_" + iterationOutputHeader)
headerItems.insert(1, "Outer_" + iterationOutputHeader)
outFile.write("\t".join(headerItems) + "\n")

for line in inFile:
    lineItems = line.rstrip().split("\t")

    description = lineItems[0].split("____")[0]
    outerIteration = lineItems[0].split("____")[1].replace(iterationOutputHeader, "")
    innerIteration = lineItems[0].split("____")[2].replace("Inner", "")

    lineItems[0] = description
    lineItems.insert(1, innerIteration)
    lineItems.insert(1, outerIteration)

    outFile.write("\t".join(lineItems) + "\n")

inFile.close()
outFile.close()
