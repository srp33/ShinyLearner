import os, sys, random

inFilePath = sys.argv[1]
outFilePath = sys.argv[2]

outFile = open(outFilePath, 'w')
outFile.write("\t".join(["Description", "Inner", "CL", "Metric", "Value"]) + "\n")

inFile = open(inFilePath)
inFile.readline()
for line in inFile:
    lineItems = line.rstrip().split("\t")
    originKeyItems = lineItems[0].split("____")
    description = originKeyItems[0]
    outerIteration = originKeyItems[1]
    innerIteration = originKeyItems[2]

    classifAlgorithm = lineItems[1]
    metric = lineItems[2]
    value = lineItems[3]

    outFile.write("\t".join([description + "____" + outerIteration, innerIteration, classifAlgorithm, metric, value]) + "\n")

inFile.close()
outFile.close()
