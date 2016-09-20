import os, sys

inFilePath = sys.argv[1]
iterationOutputHeader = sys.argv[2]
outFilePath = sys.argv[3]

outFile = open(outFilePath, 'w')
inFile = open(inFilePath)

headerItems = inFile.readline().rstrip().split("\t")
#headerItems.insert(1, "Num_Features")
#headerItems.insert(1, "Feature_Selection_Algorithm")
#headerItems.insert(1, "Ensemble_Algorithm")
headerItems.insert(1, iterationOutputHeader)
#headerItems[headerItems.index("Algorithm")] = "Classification_Algorithm"

algorithmIndex = headerItems.index("Algorithm")

outFile.write("\t".join(headerItems) + "\n")

for line in inFile:
    lineItems = line.rstrip().split("\t")

    descriptionItems = lineItems[0].split("____")
    description = descriptionItems[0]
    iteration = descriptionItems[1].replace(iterationOutputHeader, "")
    ensembleAlgorithm = descriptionItems[2]
#    fsAlgorithm = descriptionItems[3]
#    numFeatures = descriptionItems[4]

    lineItems[0] = description
#    lineItems.insert(1, numFeatures)
#    lineItems.insert(1, fsAlgorithm)
#    lineItems.insert(1, ensembleAlgorithm)
    lineItems.insert(1, iteration)

    lineItems[algorithmIndex] = ensembleAlgorithm

    outFile.write("\t".join(lineItems) + "\n")

inFile.close()
outFile.close()
