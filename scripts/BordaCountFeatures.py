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

    # Populate the dictionary with ranks for each iteration
    for i in range(len(features)):
        rank = i + 1
        feature = features[i]

        if feature in rankDict:
            rankDict[feature].append(float(rank))
        else:
            rankDict[feature] = [float(rank)]

inFile.close()

# Calculate mean ranks and build nested list
meanRanks = []
for feature, ranks in rankDict.items():
    meanRank = sum(ranks) / len(ranks)
    meanRanks.append([feature, meanRank])

meanRanks.sort(key=itemgetter(1))

outFile = open(outFilePath, 'w')
outFile.write("Feature\tMean_Rank\n")
for x in meanRanks:
    outFile.write("%s\t%.1f\n" % (x[0], x[1]))
outFile.close()
