import os, sys, glob

description = sys.argv[1]
classificationAlgorithmPaths = glob.glob(sys.argv[2])
metricFilePaths = glob.glob(sys.argv[3])

if len(classificationAlgorithmPaths) == 0:
    print "[FAILED] No classification algorithm scripts were found!"
    exit(1)

if len(metricFilePaths) == 0:
    print "[FAILED] No metric files were found!"
    exit(1)

for metricFilePath in metricFilePaths:
    metricData = [line.rstrip().split("\t") for line in file(metricFilePath)]
    headerItems = metricData.pop(0)
    metricNameIndex = headerItems.index("Metric")
    valueIndex = headerItems.index("Value")
    algorithmScriptIndex = headerItems.index("AlgorithmScript")

    uniqueAlgorithmScripts = list(set([row[algorithmScriptIndex] for row in metricData]))

    for algorithmScript in uniqueAlgorithmScripts:
        print "[TEST] Running tests for %s and %s." % (metricFilePath, algorithmScript)

        aucValues = [float(row[valueIndex]) for row in metricData if row[algorithmScriptIndex] == algorithmScript and row[metricNameIndex] == "AUROC"]
        meanAUC = sum(aucValues) / float(len(aucValues))

        if description.startswith("StrongSignal"):
            lowerThreshold = 0.9
            if meanAUC >= lowerThreshold:
                print "[OBSERVATION] The mean AUROC was %.3f for %s and %s." % (meanAUC, description, algorithmScript)
                print "[PASSED]"
            else:
                print "[OBSERVATION] The mean AUROC was %.3f for %s and %s. The expected lower threshold is %.3f." % (meanAUC, description, algorithmScript, lowerThreshold)
                print "[FAILED]"
                #exit(1)
        elif description.startswith("MediumSignal"):
            lowerThreshold = 0.6
            upperThreshold = 0.9
            if meanAUC >= lowerThreshold and meanAUC <= upperThreshold:
                print "[OBSERVATION] The mean AUROC was %.3f for %s and %s." % (meanAUC, description, algorithmScript)
                print "[PASSED]"
            else:
                print "[OBSERVATION] The mean AUROC was %.3f for %s and %s. The expected lower threshold is %.3f. The expected upper threshold is %.3f" % (meanAUC, description, algorithmScript, lowerThreshold, upperThreshold)
                print "[FAILED]"
                #exit(1)
        elif description.startswith("NoSignal"):
            upperThreshold = 0.6
            if meanAUC <= upperThreshold:
                print "[OBSERVATION] The mean AUROC was %.3f for %s and %s." % (meanAUC, description, algorithmScript)
                print "[PASSED]"
            else:
                print "[OBSERVATION] The mean AUROC was %.3f for %s and %s. The expected upper threshold is %.3f." % (meanAUC, description, algorithmScript, upperThreshold)
                print "[FAILED]"
                #exit(1)
