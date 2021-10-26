import os, sys

inFilePath = sys.argv[1]
iterationOutputHeader = sys.argv[2]
outFilePath = sys.argv[3]

outFile = open(outFilePath, 'w')
inFile = open(inFilePath)

outHeaderItems = ["Description", iterationOutputHeader, "Algorithm", "Features"]
outFile.write("\t".join(outHeaderItems) + "\n")

for line in inFile:
    lineItems = line.rstrip().split("\t")

    descriptionItems = lineItems[0].split("____")
    description = descriptionItems[0]
    iteration = descriptionItems[1].replace(iterationOutputHeader, "")
    ensembleAlgorithm = descriptionItems[2]
#    fsAlgorithm = descriptionItems[3]
#    numFeatures = descriptionItems[4]
    features = lineItems[-1]

    outLineItems = [description, iteration, ensembleAlgorithm, features]

    outFile.write("\t".join(outLineItems) + "\n")

inFile.close()
outFile.close()
