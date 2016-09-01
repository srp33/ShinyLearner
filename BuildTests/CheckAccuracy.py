import os, sys, glob

description = sys.argv[1]
classificationAlgorithmPaths = glob.glob(sys.argv[2])
metricFilePaths = glob.glob(sys.argv[3])

if len(classificationAlgorithmPaths) == 0:
    print "No classification algorithm scripts were found!"
    exit(1)

if len(metricFilePaths) == 0:
    print "No metric files were found!"
    exit(1)

for metricFilePath in metricFilePaths:
    print "Checking metric file: %s" % metricFilePath

    metricData = [line.rstrip().split("\t") for line in file(metricFilePath)]
    headerItems = metricData.pop(0)
    metricNameIndex = headerItems.index("Metric")
    valueIndex = headerItems.index("Value")

    aucValues = [float(row[valueIndex]) for row in metricData if row[metricNameIndex] == "AUROC"]
    meanAUC = sum(aucValues) / float(len(aucValues))

    if description.startswith("StrongSignal"):
        lowerThreshold = 0.9
        if meanAUC >= lowerThreshold:
            print "[PASSED]"
        else:
            print "The mean AUROC was %.3f for %s. The expected lower threshold is %.3f." % (meanAUC, description, lowerThreshold)
            print "[FAILED]"
            exit(1)
    elif description.startswith("MediumSignal"):
        lowerThreshold = 0.6
        upperThreshold = 0.9
        if meanAUC >= lowerThreshold and meanAUC <= upperThreshold:
            print "[PASSED]"
        else:
            print "The mean AUROC was %.3f for %s. The expected lower threshold is %.3f. The expected upper threshold is %.3f" % (meanAUC, description, lowerThreshold, upperThreshold)
            print "[FAILED]"
            exit(1)
    elif description.startswith("NoSignal"):
        upperThreshold = 0.6
        if meanAUC <= upperThreshold:
            print "[PASSED]"
        else:
            print "The mean AUROC was %.3f for %s. The expected upper threshold is %.3f." % (meanAUC, description, upperThreshold)
            print "[FAILED]"
            exit(1)
