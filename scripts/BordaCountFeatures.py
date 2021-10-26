import sys
from operator import itemgetter, attrgetter

inFilePath = sys.argv[1]
outFilePath = sys.argv[2]

#Description Outer_Iteration Inner_Iteration Algorithm   Features
inFile = open(inFilePath)
headerItems = inFile.readline().rstrip("\n").split("\t")

rankDict = {}

for line in inFile:
    lineItems = line.rstrip("\n").split("\t")
    features = lineItems[-1]

    if features == "ERROR":
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("Error: Feature ranks could not be summarized because at least one individual algorithm experienced an error. To troubleshoot the error, reexecute the analysis in verbose mode.")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        sys.exit(1)

    features = features.split(",")
    algorithm = lineItems[-2]

    if not algorithm in rankDict:
        rankDict[algorithm] = {}

    # Populate the dictionary with ranks for each iteration
    for i in range(len(features)):
        rank = i + 1
        feature = features[i]

        if feature in rankDict[algorithm]:
            rankDict[algorithm][feature].append(float(rank))
        else:
            rankDict[algorithm][feature] = [float(rank)]

inFile.close()

outFile = open(outFilePath, 'w')
outFile.write("Feature_Selection_Algorithm\tFeature\tMean_Rank\n")

for algorithm, algoRankDict in sorted(rankDict.items()):
    meanRanks = []
    for feature, ranks in algoRankDict.items():
        meanRank = sum(ranks) / len(ranks)
        meanRanks.append([feature, meanRank])

    meanRanks.sort(key=itemgetter(1))

    for x in meanRanks:
        outFile.write("{}\t{}\t{:.1f}\n".format(algorithm, x[0], x[1]))

outFile.close()
