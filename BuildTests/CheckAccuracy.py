import os, sys, glob

taskType = sys.argv[1]
validationType = sys.argv[2]
description = sys.argv[3]
classificationAlgorithmPaths = glob.glob(sys.argv[4])
metricFilePaths = glob.glob(sys.argv[5])
algorithmColumnName = sys.argv[6]

if len(classificationAlgorithmPaths) == 0:
    print "[FAILED] No classification algorithm scripts were found!"
    exit(1)

if len(metricFilePaths) == 0:
    print "[FAILED] No metric files were found!"
    exit(1)

successfulAlgorithms = set()
failedAlgorithms = set()

for metricFilePath in metricFilePaths:
    metricData = [line.rstrip().split("\t") for line in file(metricFilePath)]
    headerItems = metricData.pop(0)
    metricNameIndex = headerItems.index("Metric")
    valueIndex = headerItems.index("Value")
    algorithmIndex = headerItems.index(algorithmColumnName)

    uniqueAlgorithms = list(set([row[algorithmIndex] for row in metricData]))

    if len(uniqueAlgorithms) == 0:
        print "[FAILED] No algorithm scripts could be found."
        exit(1)

    for algorithm in uniqueAlgorithms:
        if "ZeroR" in algorithm:
            continue

        idText = "%s - %s - %s - %s" % (taskType, validationType, metricFilePath, algorithm)

        aucValues = [float(row[valueIndex]) for row in metricData if row[algorithmIndex] == algorithm and row[metricNameIndex] == "AUROC"]
        meanAUC = sum(aucValues) / float(len(aucValues))

        if description.startswith("StrongSignal"):
            lowerThreshold = 0.75
            if meanAUC >= lowerThreshold:
                print "[PASSED] The mean AUROC was %.3f for %s and %s. {%s}" % (meanAUC, description, algorithm, idText)
                successfulAlgorithms.add(algorithm)
            else:
                print "[FAILED] The mean AUROC was %.3f for %s and %s. The expected lower threshold is %.3f. {%s}" % (meanAUC, description, algorithm, lowerThreshold, idText)
                failedAlgorithms.add(algorithm)
        elif description.startswith("NoSignal"):
            upperThreshold = 0.7
            if meanAUC <= upperThreshold:
                print "[PASSED] The mean AUROC was %.3f for %s and %s. {%s}" % (meanAUC, description, algorithm, idText)
                successfulAlgorithms.add(algorithm)
            else:
                print "[FAILED] The mean AUROC was %.3f for %s and %s. The expected upper threshold is %.3f. {%s}" % (meanAUC, description, algorithm, upperThreshold, idText)
                failedAlgorithms.add(algorithm)

print "\n[TEST SUMMARY]\n"

if len(successfulAlgorithms) == 0:
    print "[FAILED] No algorithms successfully passed any of the tests."
    exit(1)

if len(failedAlgorithms) > 0:
    print "The following algorithm(s) failed at least once:"
    for algorithm in failedAlgorithms:
        print "  %s" % algorithm
    exit(1)
else:
    print "Tests passed!\n"
