import random, sys, os, re

if len(sys.argv) != 6:
    print "Invalid number or arguments for %s." % sys.argv[0]
    sys.exit(1)

IDFilePath = sys.argv[1]
ClassFilePath = sys.argv[2]
Prefix = sys.argv[3]
OutFilePath = sys.argv[4]
NumPermutations = sys.argv[5]
Method = sys.argv[6]
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

if Prefix == "":
    print "No prefix was specified."
    sys.exit(1)

if Method != "Normal" and Method != "Undersampling" and Method != "Oversampling" and Method != "SMOTE":
    print "That is not a valid method."
    sys.exit(1)



try:
    int(NumPermutations)
except  ValueError:
    print "%s is not a valid value for the number of permutations." % NumPermutations
    sys.exit(1)

if NumPermutations < 1:
    print "Invalid number of permutations: %s" % NumPermutations

IDFile = open(IDFilePath)
ClassFile = open(ClassFilePath)
OutputFile = open(OutFilePath, 'w')
NumPermutations = int(NumPermutations)

sampleClassDict = {}
classes = set()
for line in ClassFile:
    lineItems = line.rstrip().split("\t")
    sampleClassDict[lineItems[0]] = lineItems[1]
    classes.add(lineItems[1])

classes = sorted(list(classes))

random.seed(0)
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
    for val in range(0, NumPermutations):
        training = []
        test = []

        for className in classes:
            classSamples = [sampleID for sampleID in sampleIDs if sampleClassDict[sampleID] == className]
            random.shuffle(classSamples)
            classTrain = []
            classTest = []
            while len(classSamples) > 0:
                classTest.append(classSamples.pop(0))
                if len(classSamples) == 0:
                    break
                classTrain.append(classSamples.pop(0))
                if len(classSamples) == 0:
                    break
                classTrain.append(classSamples.pop(0))
                if len(classSamples) == 0:
                    break
            training.extend(classTrain)
            test.extend(classTest)
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


#Undersampling Method:
#---ask user which method they would like to use in command line
#---if more than 2 classes in undersampling method, reject user
#---ONLY apply method to training set, not test
#---figure out which class is minority class
#---take number of minority class and compare to same number of samples from the majority class
#---repeat action x number of times...maybe input from user???
#---

OutputFile.write(test_and_training)

ClassFile.close()
IDFile.close()
OutputFile.close()
