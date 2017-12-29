import random, sys, os, re

if len(sys.argv) != 7:
    print("Invalid number or arguments for {}.".format(sys.argv[0]))
    sys.exit(1)

IDFilePath = sys.argv[1]
ClassFilePath = sys.argv[2]
Prefix = sys.argv[3]
OutFilePath = sys.argv[4]
NumPermutations = sys.argv[5]
Method = sys.argv[6]

if Prefix == "":
    print("No prefix was specified.")
    sys.exit(1)

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

NumPermutations = int(NumPermutations)

try:
    int(NumPermutations)
except  ValueError:
    print("{} is not a valid value for the number of permutations.".format(NumPermutations))
    sys.exit(1)

if NumPermutations < 1:
    print("Invalid number of permutations: {}".format(NumPermutations))
    sys.exit(1)

if Method != "Normal" and Method != "UnderSampling" and Method != "OverSampling" and Method != "SMOTE":
    print("That is not a valid method.")
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

        intersectSamples = set(training).intersection(test)
        if len(intersectSamples) > 0:
            print("The following samples overlapped between the training and test set, which is invalid.")
            for s in intersectSamples:
                print(s)
            sys.exit(1)

        total_assigned = len(training) + len(test)
        if total != total_assigned:
            print("The number of samples assigned to training and test [{}] is not equal to the number of input samples [{}].".format(total_assigned, total))
            sys.exit(1)
        iteration += 1

        test_and_training += description + "____{}{}".format(Prefix, iteration)

        test_and_training +=  "\t{}\t{}\n".format(",".join(training), ",".join(test))
        for val in training:
            if val not in sampleIDs:
                print("The IDs in the nested validation are not the same as the previous iteration.")
                sys.exit(1)
        for val in test:
            if val not in sampleIDs:
                print("The IDs in the nested validation are not the same as the previous iteration.")
                sys.exit(1)
if Method == "Normal":
    OutputFile.write(test_and_training)

def UnderSampling():
    firstClass = 0
    secondClass = 0
    majorityClass = ""
    minorityClass = ""
    majClassLength = 0
    minClassLength = 0
    majorityClassList = []
    minorityClassList = []

    if len(classes) != 2:
        print("invalid number of classes in data set.")
        sys.exit(1)
    for key in sampleClassDict.keys():
        if key in training:
            if sampleClassDict[key] == classes[0]:
                firstClass += 1
            elif sampleClassDict[key] == classes[1]:
                secondClass += 1
    if firstClass > secondClass:
        majorityClass = classes[0]
        majClassLength = firstClass
        minorityClass = classes[1]
        minClassLength = secondClass
    elif secondClass > firstClass:
        majorityClass = classes[1]
        majClassLength = secondClass
        minortyClass = classes[0]
        minClassLength = firstClass

    for key in sampleClassDict.keys():
        if key in training:
            if sampleClassDict[key] == majorityClass:
                majorityClassList.append(key)
            elif sampleClassDict[key] == minorityClass:
                minorityClassList.append(key)

    MajorityAndMinority = ""

    iteration = 0
    for val in range(NumPermutations):
        random.shuffle(majorityClassList)
        iteration += 1
        majComparisonList = []

        for val in range(minClassLength):
            majComparisonList.append(majorityClassList[val])


        MajorityAndMinority += description + "____{}{}".format(Prefix, iteration)

        MajorityAndMinority += "\t{}\t{}\n".format(",".join(majComparisonList), ",".join(minorityClassList))
    OutputFile.write(MajorityAndMinority)

    return

if Method == "UnderSampling":
    UnderSampling()
#elif Method = "OverSampling":








ClassFile.close()
IDFile.close()
OutputFile.close()
