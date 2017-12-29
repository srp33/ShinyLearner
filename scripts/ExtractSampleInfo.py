import sys, os, glob, gzip

if len(sys.argv) != 5:
    print("Invalid number or arguments for {}.".format(sys.argv[0]))
    sys.exit(1)

inFilePath = sys.argv[1]
prefix = sys.argv[2]
outSamplesFilePath = sys.argv[3]
outClassesFilePath = sys.argv[4]

if not os.path.exists(inFilePath):
    print("File " + inFilePath + " does not exist.")
    sys.exit(1)

if inFilePath == outSamplesFilePath or inFilePath == outClassesFilePath:
    print("One or more file names were repeated.")
    sys.exit(1)

if not os.path.exists(os.path.dirname(outSamplesFilePath)):
    print("Creating directory at {}".format(os.path.dirname(outSamplesFilePath)))
    os.makedirs(os.path.dirname(outSamplesFilePath))

if not os.path.exists(os.path.dirname(outClassesFilePath)):
    print("Creating directory at {}".format(os.path.dirname(outClassesFilePath)))
    os.makedirs(os.path.dirname(outClassesFilePath))

def openFile(inFilePath):
    if inFilePath.endswith(".gz"):
        inFile = gzip.open(inFilePath)
    else:
        inFile = open(inFilePath)

    return inFile

sampleClassDict = {}

inFile = openFile(inFilePath)

dataPointNames = inFile.readline().decode().rstrip().split("\t")[1:]
classIndex = dataPointNames.index("Class")

for line in inFile:
    lineItems = line.decode().rstrip().split("\t")
    sampleID = lineItems.pop(0)
    classValue = lineItems[classIndex]

    sampleClassDict[sampleID] = classValue

inFile.close()

sampleIDs = sorted(list(sampleClassDict.keys()))

outSamplesFile = open(outSamplesFilePath, 'w')
outSamplesFile.write(prefix + "\t" + ",".join(sampleIDs) + "\t")
outSamplesFile.close()

outClassesFile = open(outClassesFilePath, 'w')
for sampleID in sampleIDs:
    outClassesFile.write("{}\t{}\n".format(sampleID, sampleClassDict[sampleID]))
outClassesFile.close()
