import os, sys, glob
from collections import defaultdict

selectedFeaturesFilePath = sys.argv[1]
trainTestFilePath = sys.argv[2]
numFeaturesFilePath = sys.argv[3]
outFilePath = sys.argv[4]

numFeaturesDict = {}
if os.path.exists(numFeaturesFilePath):
    numFeaturesFile = open(numFeaturesFilePath)
    for line in numFeaturesFile:
        lineItems = line.rstrip().split("\t")
        numFeaturesDict[lineItems[0]] = int(lineItems[1])
    numFeaturesFile.close()

# This file has Description, Algorithm, Selected features
algorithmDict = {}
featuresDict = {}
selectedFeaturesFile = open(selectedFeaturesFilePath)
selectedFeaturesFile.readline()
for line in selectedFeaturesFile:
    lineItems = line.rstrip().split("\t")
    algorithmDict[lineItems[0]] = lineItems[1]
    featuresDict[lineItems[0]] = lineItems[2].split(",")
selectedFeaturesFile.close()

outFile = open(outFilePath, 'w')

# This file has Train/Test key, Training instances, Test instances, algorithm
trainTestFile = open(trainTestFilePath)
for line in trainTestFile:
    lineItems = line.rstrip().split("\t")

    algorithm = algorithmDict[lineItems[0]]

    numFeatures = numFeaturesDict[lineItems[0]]
    features = ",".join(featuresDict[lineItems[0]][:numFeatures])

    outItems = list(lineItems[:4])
    outItems[0] = "{}____{}____{}".format(outItems[0], algorithm, numFeatures)
    outItems.append(features)
    outFile.write("\t".join(outItems) + "\n")

trainTestFile.close()

outFile.close()
