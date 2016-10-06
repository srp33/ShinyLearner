import os, sys, glob
from operator import itemgetter, attrgetter

inFilePatterns = sys.argv[1].split(",")
outFilePaths = sys.argv[2].split(",")

def saveOutputFile(inFilePattern, outFilePath):
    if outFilePath != "":
        inFilePaths = glob.glob(inFilePattern)
        outFile = open(outFilePath, 'w')
        outItems = []

        for inFilePath in inFilePaths:
            iteration = os.path.basename(os.path.dirname(inFilePath))

            inFile = open(inFilePath)
            headerLine = inFile.readline()

            if inFilePath == inFilePaths[0]:
                headerItems = headerLine.rstrip().split("\t")
                headerItems.insert(1, "Iteration")
                outFile.write("\t".join(headerItems) + "\n")

            for line in inFile:
                lineItems = line.rstrip().split("\t")
                lineItems.insert(1, int(iteration))
                outItems.append(lineItems)

            inFile.close()

        #outItems.sort(key=itemgetter(1))
        for lineItems in outItems:
            outFile.write("\t".join([str(x) for x in lineItems]) + "\n")

        outFile.close()

for i in range(len(inFilePatterns)):
    saveOutputFile(inFilePatterns[i], outFilePaths[i])
