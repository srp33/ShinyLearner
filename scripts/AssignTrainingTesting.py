import random, sys, os, re, math

if len(sys.argv) != 8:
    print "Invalid number or arguments for %s." % sys.argv[0]
    sys.exit(1)

IDFilePath = sys.argv[1]
ClassFilePath = sys.argv[2]
Prefix = sys.argv[3]
OutFilePath = sys.argv[4]
NumIterations = sys.argv[5]
RandomSeed = sys.argv[6]
ProportionTrain = sys.argv[7]

if Prefix == "":
    print "No prefix was specified."
    sys.exit(1)

if not os.path.exists(IDFilePath):
    print "File " + IDFilePath + " does not exist."
    sys.exit(1)

if not os.path.exists(ClassFilePath):
    print "File " + ClassFilePath + " does not exist."
    sys.exit(1)

if IDFilePath == ClassFilePath or IDFilePath == OutFilePath or ClassFilePath == OutFilePath:
    print "Repeated file names"
    sys.exit(1)
if not os.path.exists(os.path.dirname(OutFilePath)):
    print "Creating directory at %s." % os.path.dirname(OutFilePath)
    os.makedirs(os.path.dirname(OutFilePath))

try:
    int(NumIterations)
except  ValueError:
    print "%s is not a valid value for the number of iterations." % NumIterations
    sys.exit(1)

NumIterations = int(NumIterations)

if NumIterations < 1:
    print "Invalid number of iterations: %s" % NumIterations
    sys.exit(1)

try:
    int(RandomSeed)
except  ValueError:
    print "%s is not a valid value for the random seed." % RandomSeed
    sys.exit(1)

RandomSeed = int(RandomSeed)

try:
    float(ProportionTrain)
except  ValueError:
    print "%s is not a valid value for the proportion of training samples." % ProportionTrain
    sys.exit(1)

ProportionTrain = float(ProportionTrain)

if ProportionTrain < 0.25 or ProportionTrain > 0.9:
    print "Invalid value specified for --train-proportion: %s." % ProportionTrain
    sys.exit(1)

IDFile = open(IDFilePath)
ClassFile = open(ClassFilePath)
OutputFile = open(OutFilePath, 'w')

sampleClassDict = {}
classes = set()
for line in ClassFile:
    lineItems = line.rstrip().split("\t")
    sampleClassDict[lineItems[0]] = lineItems[1]
    classes.add(lineItems[1])

classes = sorted(list(classes))

random.seed(RandomSeed)
test_and_training = ""

for line in IDFile:
    if line.rstrip() == "":
        continue

    lineItems = line.rstrip().split("\t")
    description = lineItems[0]
    sampleIDs = lineItems[1].split(',')
    sampleIDs = list(set(sampleIDs) & set(sampleClassDict.keys()))

    total = len(sampleIDs)
    iteration = 0
    for val in range(0, NumIterations):
        training = []
        test = []

        for className in classes:
            classSamples = [sampleID for sampleID in sampleIDs if sampleClassDict[sampleID] == className]
            random.shuffle(classSamples)

            numTrain = int(math.floor(float(len(classSamples)) * ProportionTrain))

            training.extend(classSamples[:numTrain])
            test.extend(classSamples[numTrain:])

#        print "The number of samples in the class file was %i." % len(SAMPLE_IDS)
#        print "The number of samples in the gene-expression file was %i." % len(EXPRESSION_IDS)
#        print "The number of samples in training set is %i." % len(training)
#        print "The number of samples in test set is %i." % len(test)

        intersectSamples = set(training).intersection(test)
        if len(intersectSamples) > 0:
            print "The following samples overlapped between the training and test set, which is invalid."
            for s in intersectSamples:
                print s
            sys.exit(1)

        total_assigned = len(training) + len(test)
        if total != total_assigned:
            print "The number of samples assigned to training and test [%i] is not equal to the number of input samples [%i]." % (total_assigned, total)
            sys.exit(1)
        iteration += 1

        test_and_training += description + "____%s%i" % (Prefix, iteration)

        test_and_training +=  "\t%s\t%s\n" % (",".join(training), ",".join(test))
        for val in training:
            if val not in sampleIDs:
                print "The IDs in the nested validation are not the same as the previous iteration."
                sys.exit(1)
        for val in test:
            if val not in sampleIDs:
                print "The IDs in the nested validation are not the same as the previous iteration."
                sys.exit(1)

OutputFile.write(test_and_training)

ClassFile.close()
IDFile.close()
OutputFile.close()
