import os, sys, glob
from collections import defaultdict

selectedFeaturesFilePath = sys.argv[1]
trainTestFilePath = sys.argv[2]
numFeaturesOptions = [int(x) for x in sys.argv[3].split(",")]
outFilePath = sys.argv[4]

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
for line in file(trainTestFilePath):
    lineItems = line.rstrip().split("\t")

    for fsAlgorithm in featuresDict[lineItems[0]]:
        for numFeatures in numFeaturesOptions:
            features = featuresDict[lineItems[0]][fsAlgorithm]
            features = ",".join(features[:numFeatures])

            if len(features) < numFeatures:
                continue

            outItems = list(lineItems[:4])
            outItems[0] = "%s____%s____%i" % (outItems[0], fsAlgorithm, numFeatures)
            outItems.append(features)
            outLines.append("\t".join(outItems) + "\n")

if len(outLines) == 0:
    print "No inner selected features were available."
    sys.exit(1)

outFile = open(outFilePath, 'w')
for line in outLines:
    outFile.write(line)
outFile.close()
