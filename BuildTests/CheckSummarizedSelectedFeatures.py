import os, sys, glob

inFilePath = sys.argv[1]

inFile = open(inFilePath)
inFile.readline()

dataDict = {}
for line in inFile:
    lineItems = line.rstrip().split("\t")
    dataDict[lineItems[0]] = float(lineItems[1])

inFile.close()

if not os.path.exists(inFilePath):
    print("[FAILED] No file exists at {}".format(inFilePath))
    exit(1)

if "StrongSignal" in inFilePath:
    lowerThreshold = 0
    upperThreshold = 30
elif "NoSignal" in inFilePath:
    lowerThreshold = 20
    upperThreshold = 100000000

featureNames = set()
for i in range(1, 6):
    featureNames.add("Feature{}".format(i))
for i in range(51, 56):
    featureNames.add("Feature{}_Low".format(i))
    featureNames.add("Feature{}_Medium".format(i))

meanRanks = [dataDict[featureName] for featureName in featureNames]
meanMeanRank = sum(meanRanks) / len(meanRanks)
success = meanMeanRank > lowerThreshold and meanMeanRank <= upperThreshold

if success:
    print("[PASSED] The mean summarized rank for {} was {:.2f}.".format(inFilePath, meanMeanRank))
else:
    print("[FAILED] The mean summarized rank for {} was {:.2f} but should have been between {:.2f} and {:.2f}.".format(inFilePath, meanMeanRank, lowerThreshold, upperThreshold))
    exit(1)
