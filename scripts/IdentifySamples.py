import sys, os, glob, gzip

if len(sys.argv) != 5:
    print "Invalid number or arguments for %s." % sys.argv[0]
    sys.exit(1)

inFilePath = sys.argv[1]
prefix = sys.argv[2]
outSamplesFilePath = sys.argv[3]
outClassesFilePath = sys.argv[4]

inFilePaths = []
for inFilePattern in inFilePath.split(","):
    inFilePaths.extend(glob.glob(inFilePattern))

#if prefix == "":
#    print "No prefix was specified."
#    sys.exit(1)

if len(set(inFilePaths)) != len(inFilePaths):
    print "One or more file names were repeated."
    sys.exit(1)

for inFilePath in inFilePaths:
    if not os.path.exists(inFilePath):
        print "File " + inFilePath + " does not exist."
        sys.exit(1)

    if inFilePath == outSamplesFilePath or inFilePath == outClassesFilePath:
        print "One or more file names were repeated."
        sys.exit(1)

if len(inFilePaths) == 0:
    print "No data files were found."
    sys.exit(1)

if not os.path.exists(os.path.dirname(outSamplesFilePath)):
    print "Creating directory at %s" % os.path.dirname(outSamplesFilePath)
    os.makedirs(os.path.dirname(outSamplesFilePath))

if not os.path.exists(os.path.dirname(outClassesFilePath)):
    print "Creating directory at %s" % os.path.dirname(outClassesFilePath)
    os.makedirs(os.path.dirname(outClassesFilePath))

def openFile(inFilePath):
    if inFilePath.endswith(".gz"):
        inFile = gzip.open(inFilePath)
    else:
        inFile = open(inFilePath)

    return inFile

commonSampleIDs = set()
sampleClassDict = {}
for inFilePath in inFilePaths:
    inFile = openFile(inFilePath)
    sampleIDs = [line.rstrip().split("\t")[0] for line in inFile][1:]
    inFile.close()

    if len(commonSampleIDs) == 0:
        commonSampleIDs = set(sampleIDs)
    else:
        commonSampleIDs = commonSampleIDs & set(sampleIDs)

    inFile = openFile(inFilePath)

    headerItems = inFile.readline().rstrip().split("\t")

    classIndex = None
    if "Class" in headerItems:
        classIndex = headerItems.index("Class")

    for line in inFile:
        lineItems = line.rstrip().split("\t")
        sampleID = lineItems[0]

        if classIndex != None:
            sampleClassDict[sampleID] = lineItems[classIndex]

    inFile.close()

commonSampleIDs = sorted(list(commonSampleIDs))

for sampleID in commonSampleIDs:
    if sampleID not in sampleClassDict:
        print "There is no class value in any input file for sample %s." % sampleID
        exit(1)

outSamplesFile = open(outSamplesFilePath, 'w')
print >> outSamplesFile, prefix + "\t" + ",".join(commonSampleIDs) + "\t"
outSamplesFile.close()

outClassesFile = open(outClassesFilePath, 'w')
for sampleID in commonSampleIDs:
    outClassesFile.write("%s\t%s\n" % (sampleID, sampleClassDict[sampleID]))
outClassesFile.close()
