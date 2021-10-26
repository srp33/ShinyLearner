import os, sys

inFilePath = sys.argv[1]
iterationOutputHeader = sys.argv[2]
outFilePath = sys.argv[3]

outFile = open(outFilePath, 'w')
inFile = open(inFilePath)

headerItems = inFile.readline().rstrip().split("\t")
#headerItems.insert(1, "Ensemble_Algorithm")
headerItems.insert(1, iterationOutputHeader)
outFile.write("\t".join(headerItems) + "\n")

algorithmIndex = headerItems.index("Algorithm")

for line in inFile:
    lineItems = line.rstrip().split("\t")

    description = lineItems[0].split("____")[0]
    iteration = lineItems[0].split("____")[1].replace(iterationOutputHeader, "")
    ensembleAlgorithm = lineItems[0].split("____")[2]

    lineItems[0] = description
    #lineItems.insert(1, ensembleAlgorithm)
    lineItems.insert(1, iteration)

    lineItems[algorithmIndex] = ensembleAlgorithm

    outFile.write("\t".join(lineItems) + "\n")

inFile.close()
outFile.close()
