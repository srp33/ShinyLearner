import os, sys, glob

description = sys.argv[1]
classificationAlgorithmPaths = glob.glob(sys.argv[2])
metricFilePaths glob.glob(sys.argv[3])

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

    if "Strong" in description:
        threshold = 0.9
        if meanAUC >= threshold:
            print "[PASSED]"
        else:
            print "The mean AUROC was %.3f for %s. The expected lower threshold is %.3f." % (meanAUC, description, threshold)
            print "[FAILED]"
            exit(1)
