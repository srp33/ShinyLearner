import os, sys, random

inFilePath = sys.argv[1]
outFilePath = sys.argv[2]

outFile = open(outFilePath, 'w')
outFile.write("\t".join(["Description", "Inner", "FS", "NumFeatures", "CL", "Metric", "Value"]) + "\n")

#StrongSignal_Small_Both____Outer1____Inner1____/Users/srp33/Dropbox/ML-Flex-Lite/AlgorithmScripts/FeatureSelection/arff/weka__info_gain____5Features	/Users/srp33/Dropbox/ML-Flex-Lite/AlgorithmScripts/Classification/arff/weka__rules__one_r	Weighted average AUC	1.0
inFile = open(inFilePath)
inFile.readline()
for line in inFile:
    lineItems = line.rstrip().split("\t")
    originKeyItems = lineItems[0].split("____")
    description = originKeyItems[0]
    outerIteration = originKeyItems[1]
    innerIteration = originKeyItems[2]
    fsAlgorithm = originKeyItems[3]
    numFeatures = originKeyItems[4]

    classifAlgorithm = lineItems[1]
    metric = lineItems[2]
    value = lineItems[3]

    outFile.write("\t".join([description + "____" + outerIteration, innerIteration, fsAlgorithm, numFeatures, classifAlgorithm, metric, value]) + "\n")

inFile.close()
outFile.close()
