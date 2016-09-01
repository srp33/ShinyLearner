import os, sys

inFilePath = sys.argv[1]
iterationOutputHeader = sys.argv[2]
outFilePath = sys.argv[3]

outFile = open(outFilePath, 'w')
inFile = open(inFilePath)
#StrongSignal_Small_Both____Iteration1____Nested_Select_Best____/Users/srp33/Dropbox/ML-Flex-Lite/AlgorithmScripts/FeatureSelection/arff/weka__info_gain____20	/Users/srp33/Dropbox/ML-Flex-Lite/AlgorithmScripts/Classification/arff/weka__rules__one_r	Weighted average AUC	1.0

headerItems = inFile.readline().rstrip().split("\t")
headerItems.insert(1, "Num_Features")
headerItems.insert(1, "Feature_Selection_AlgorithmScript")
headerItems.insert(1, "Nested_Algorithm")
headerItems.insert(1, iterationOutputHeader)
headerItems[headerItems.index("AlgorithmScript")] = "Classification_AlgorithmScript"
outFile.write("\t".join(headerItems) + "\n")

for line in inFile:
    lineItems = line.rstrip().split("\t")

    descriptionItems = lineItems[0].split("____")
    description = descriptionItems[0]
    iteration = descriptionItems[1].replace(iterationOutputHeader, "")
    nestedAlgorithm = descriptionItems[2]
    fsAlgorithm = descriptionItems[3]
    numFeatures = descriptionItems[4]

    lineItems[0] = description
    lineItems.insert(1, numFeatures)
    lineItems.insert(1, fsAlgorithm)
    lineItems.insert(1, nestedAlgorithm)
    lineItems.insert(1, iteration)

    outFile.write("\t".join(lineItems) + "\n")

inFile.close()
outFile.close()
