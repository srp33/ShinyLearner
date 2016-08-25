import os, sys, random

inFilePath = sys.argv[1]
outFilePath = sys.argv[2]

outFile = open(outFilePath, 'w')
outFile.write("\t".join(["Description", "Inner", "CL", "ParameterDescription", "Metric", "Value"]) + "\n")

inFile = open(inFilePath)
inFile.readline()
for line in inFile:
    lineItems = line.rstrip().split("\t")
    originKeyItems = lineItems[0].split("____")
    description = originKeyItems[0]
    outerIteration = originKeyItems[1]
    innerIteration = originKeyItems[2]

    classifAlgorithm = lineItems[1]
    parameterDescription = lineItems[2]
    metric = lineItems[3]
    value = lineItems[4]

    outFile.write("\t".join([description + "____" + outerIteration, innerIteration, classifAlgorithm, parameterDescription, metric, value]) + "\n")

inFile.close()
outFile.close()
