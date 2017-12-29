import random, sys, os, re

if len(sys.argv) != 7:
    print("Invalid number or arguments for {}.".format(sys.argv[0]))
    sys.exit(1)

IDFilePath = sys.argv[1]
ClassFilePath = sys.argv[2]
Prefix = sys.argv[3]
OutFilePath = sys.argv[4]
NumFolds = sys.argv[5]
RandomSeed = sys.argv[6]

if not os.path.exists(IDFilePath):
    print("File " + IDFilePath + " does not exist.")
    sys.exit(1)

if not os.path.exists(ClassFilePath):
    print("File " + ClassFilePath + " does not exist.")
    sys.exit(1)

if IDFilePath == ClassFilePath or IDFilePath == OutFilePath or ClassFilePath == OutFilePath:
    print("Repeated file names")
    sys.exit(1)

if not os.path.exists(os.path.dirname(OutFilePath)):
    print("Creating directory at {}.".format(os.path.dirname(OutFilePath)))
    os.makedirs(os.path.dirname(OutFilePath))

if Prefix == "":
    print("No prefix was specified.")
    sys.exit(1)

try:
    int(NumFolds)
except  ValueError:
    print("{} is not a valid value for the number of folds.".format(NumFolds))
    sys.exit(1)

NumFolds = int(NumFolds)

if NumFolds < 0 or NumFolds == 1:
    print("Invalid number of folds: {}".format(NumFolds))
    sys.exit(1)

try:
    int(RandomSeed)
except  ValueError:
    print("{} is not a valid value for the random seed.".format(RandomSeed))
    sys.exit(1)

RandomSeed = int(RandomSeed)

IDFile = open(IDFilePath)
ClassFile = open(ClassFilePath)
OutputFile = open(OutFilePath, 'w')

def checkSamples(trainIDs, testIDs, expectedTotal):
    intersectSamples = set(trainIDs).intersection(testIDs)
    if len(intersectSamples) > 0:
        print("The following samples overlapped between the training and test set, which is invalid.")
        print(",".join(list(intersectSamples)))
        sys.exit(1)

    total_assigned = len(trainIDs) + len(testIDs)

    if total != total_assigned:
        print("The number of samples assigned to the training and test sets [{}] is not equal to the number of input samples [{}].".format(total_assigned, expectedTotal))
        sys.exit(1)

def writeOutputFile(description, fold, trainIDs, testIDs):
    OutputFile.write("{}\t{}\t{}\n".format(("{}____{}{}".format(description, Prefix, fold)), ",".join(trainIDs), ",".join(testIDs)))

sampleClassDict = {}
classes = set()
for line in ClassFile:
    lineItems = line.rstrip().split("\t")
    sampleClassDict[lineItems[0]] = lineItems[1]
    classes.add(lineItems[1])

classes = sorted(list(classes))

random.seed(RandomSeed)

for line in IDFile:
    if line.rstrip() == "":
        continue

    lineItems = line.rstrip().split("\t")
    description = lineItems[0]
    sampleIDs = lineItems[1].split(',')
    sampleIDs = sorted(list(set(sampleIDs) & set(sampleClassDict.keys())))

    total = len(sampleIDs)

    if NumFolds == 0 or NumFolds >= total: # Leave-one-out cross validation
        sampleIDs = sorted(sampleIDs)
        for i in range(total):
            testIDs = [sampleIDs[i]]
            trainIDs = [sampleIDs[j] for j in range(total) if j != i]

            checkSamples(testIDs, trainIDs, total)
            writeOutputFile(description, i+1, sorted(trainIDs), sorted(testIDs))
    else: # Regular cross validation
        foldDict = {}

        fold = 1
        for className in classes:
            classSamples = [sampleID for sampleID in sampleIDs if sampleClassDict[sampleID] == className]
            random.shuffle(classSamples)

            while len(classSamples) != 0:
                foldDict[fold] = foldDict.setdefault(fold, []) + [classSamples.pop(0)]

                fold += 1
                if fold > NumFolds:
                    fold = 1

        for fold in range(1, NumFolds + 1):
            testIDs = foldDict[fold]
            trainIDs = list(set(sampleIDs) - set(testIDs))

            checkSamples(testIDs, trainIDs, total)
            writeOutputFile(description, fold, sorted(trainIDs), sorted(testIDs))

ClassFile.close()
IDFile.close()
OutputFile.close()
