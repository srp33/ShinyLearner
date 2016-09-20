import os, sys

inFilePath = sys.argv[1]
iterationOutputHeader = sys.argv[2]
outFilePath = sys.argv[3]

outFile = open(outFilePath, 'w')
inFile = open(inFilePath)
#StrongSignal_Small_Both____Iteration1____Ensemble_Select_Best____/Users/srp33/Dropbox/ML-Flex-Lite/AlgorithmScripts/FeatureSelection/arff/weka__info_gain____20	/Users/srp33/Dropbox/ML-Flex-Lite/AlgorithmScripts/Classification/arff/weka__rules__one_r	Weighted average AUC	1.0

headerItems = inFile.readline().rstrip().split("\t")
headerItems.insert(1, "Num_Features")
headerItems.insert(1, "Feature_Selection_Algorithm")
headerItems.insert(1, "Inner_" + iterationOutputHeader)
headerItems.insert(1, "Outer_" + iterationOutputHeader)
headerItems[headerItems.index("Algorithm")] = "Classification_Algorithm"
outFile.write("\t".join(headerItems) + "\n")

for line in inFile:
    lineItems = line.rstrip().split("\t")

    descriptionItems = lineItems[0].split("____")
    description = descriptionItems[0]
    outerIteration = descriptionItems[1].replace(iterationOutputHeader, "")
    innerIteration = descriptionItems[2].replace("Inner", "")
    fsAlgorithm = descriptionItems[3]
    numFeatures = descriptionItems[4]

    lineItems[0] = description
    lineItems.insert(1, numFeatures)
    lineItems.insert(1, fsAlgorithm)
    lineItems.insert(1, innerIteration)
    lineItems.insert(1, outerIteration)

    outFile.write("\t".join(lineItems) + "\n")

inFile.close()
outFile.close()
