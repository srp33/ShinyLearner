import os, sys, random
from collections import defaultdict

inFilePath = sys.argv[1]
queryMetric = sys.argv[2]
outFilePath = sys.argv[3]

resultsDict = defaultdict(lambda: {})

#StrongSignal_Small_Both____Outer1____Inner1____/Users/srp33/Dropbox/ML-Flex-Lite/AlgorithmScripts/FeatureSelection/arff/weka__info_gain____5Features	/Users/srp33/Dropbox/ML-Flex-Lite/AlgorithmScripts/Classification/arff/weka__rules__one_r	Weighted average AUC	1.0
for line in file(inFilePath):
    lineItems = line.rstrip().split("\t")

    metric = lineItems[2]
    if metric != queryMetric:
        continue

    clAlgorithm = lineItems[1]
    value = float(lineItems[3])

    originKeyItems = lineItems[0].split("____")
    description = originKeyItems[0]
    outerIteration = originKeyItems[1]
    innerIteration = originKeyItems[2]
    fsAlgorithm = originKeyItems[3]
    numFeatures = originKeyItems[4]

    shortKey = "____".join([description, outerIteration])
    longKey = "____".join([description, outerIteration, innerIteration, fsAlgorithm, numFeatures, clAlgorithm])

    resultsDict[shortKey][value] = longKey

outFile = open(outFilePath, 'w')
for shortKey in sorted(resultsDict.keys()):
    topScore = max(resultsDict[shortKey])
    candidateLongKeys = [resultsDict[shortKey][x] for x in resultsDict[shortKey].keys() if x == topScore]
    random.shuffle(candidateLongKeys)
    selectedLongKey = candidateLongKeys[0]

    outFile.write("%s\t%s\n" % (shortKey, "\t".join(selectedLongKey.replace(shortKey + "____", "").split("____")[1:])))
outFile.close()
