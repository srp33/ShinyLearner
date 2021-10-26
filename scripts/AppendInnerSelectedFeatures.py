import os, sys, glob
from collections import defaultdict

selectedFeaturesFilePath = sys.argv[1]
trainTestFilePath = sys.argv[2]
numFeaturesOptions = sorted([int(x) for x in sys.argv[3].split(",")])
outFilePath = sys.argv[4]

def checkNumFeaturesOptions(numFeaturesOptions, features):
    revisedOptions = []

    for option in numFeaturesOptions:
        revisedOptions.append(option)

        if option > len(features):
            break

    return revisedOptions

# This file has Description, Algorithm, Selected features
featuresDict = defaultdict(lambda: {})
selectedFeaturesFile = open(selectedFeaturesFilePath)
selectedFeaturesFile.readline()

for line in selectedFeaturesFile:
    lineItems = line.rstrip().split("\t")
    features = lineItems[2].split(",")

    if features == ["ERROR"]:
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Error: At least one individual algorithm experienced an error when attempting to select features. To troubleshoot the error, reexecute ShinyLearner in verbose mode.")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        sys.exit(1)

    featuresDict[lineItems[0]][lineItems[1]] = features

selectedFeaturesFile.close()

outLines = []

# This file has Train/Test key, Training instances, Test instances, algorithm
trainTestFile = open(trainTestFilePath)
for line in trainTestFile:
    lineItems = line.rstrip().split("\t")

    for fsAlgorithm in featuresDict[lineItems[0]]:
        features = featuresDict[lineItems[0]][fsAlgorithm]

        # Find which options are relevant for this dataset
        numFeaturesOptions2 = checkNumFeaturesOptions(numFeaturesOptions, features)

        for numFeatures in numFeaturesOptions2:
            outFeatures = ",".join(features[:numFeatures])

            outItems = list(lineItems[:4])
            outItems[0] = "{}____{}____{}".format(outItems[0], fsAlgorithm, numFeatures)
            outItems.append(outFeatures)
            outLines.append("\t".join(outItems) + "\n")

trainTestFile.close()

if len(outLines) == 0:
    print("No inner selected features were available.")
    sys.exit(1)

outFile = open(outFilePath, 'w')
for line in outLines:
    outFile.write(line)
outFile.close()
