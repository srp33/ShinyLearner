import os, sys

inFilePath = sys.argv[1]
iterationOutputHeader = sys.argv[2]
outFilePath = sys.argv[3]

outFile = open(outFilePath, 'w')
inFile = open(inFilePath)
#StrongSignal_Small_Both____Iteration1____Nested_Select_Best	/Users/srp33/Dropbox/ML-Flex-Lite/AlgorithmScripts/Classification/arff/weka__rules__one_r	Weighted average AUC	1.0

headerItems = inFile.readline().rstrip().split("\t")
headerItems.insert(1, "Nested_Algorithm")
headerItems.insert(1, iterationOutputHeader)
outFile.write("\t".join(headerItems) + "\n")

for line in inFile:
    lineItems = line.rstrip().split("\t")

    description = lineItems[0].split("____")[0]
    iteration = lineItems[0].split("____")[1].replace(iterationOutputHeader, "")
    nestedAlgorithm = lineItems[0].split("____")[2]

    lineItems[0] = description
    lineItems.insert(1, nestedAlgorithm)
    lineItems.insert(1, iteration)

    outFile.write("\t".join(lineItems) + "\n")

inFile.close()
outFile.close()
