import os, sys, glob

taskType = sys.argv[1]
validationType = sys.argv[2]
description = sys.argv[3]
classificationAlgorithmPaths = glob.glob(sys.argv[4])
metricFilePaths = glob.glob(sys.argv[5])
algorithmScriptColumnName = sys.argv[6]

if len(classificationAlgorithmPaths) == 0:
    print "[FAILED] No classification algorithm scripts were found!"
    exit(1)

if len(metricFilePaths) == 0:
    print "[FAILED] No metric files were found!"
    exit(1)

failedAlgorithms = set()

for metricFilePath in metricFilePaths:
    metricData = [line.rstrip().split("\t") for line in file(metricFilePath)]
    headerItems = metricData.pop(0)
    metricNameIndex = headerItems.index("Metric")
    valueIndex = headerItems.index("Value")
    algorithmScriptIndex = headerItems.index(algorithmScriptColumnName)

    uniqueAlgorithmScripts = list(set([row[algorithmScriptIndex] for row in metricData]))

    if len(uniqueAlgorithmScripts) == 0:
        print "[FAILED] No algorithm scripts could be found."
        exit(1)

    for algorithmScript in uniqueAlgorithmScripts:
        if "ZeroR" in algorithmScript:
            continue

        idText = "%s - %s - %s - %s" % (taskType, validationType, metricFilePath, algorithmScript)

        aucValues = [float(row[valueIndex]) for row in metricData if row[algorithmScriptIndex] == algorithmScript and row[metricNameIndex] == "AUROC"]
        meanAUC = sum(aucValues) / float(len(aucValues))

        if description.startswith("StrongSignal"):
            lowerThreshold = 0.9
            if meanAUC >= lowerThreshold:
                print "[PASSED] The mean AUROC was %.3f for %s and %s. {%s}" % (meanAUC, description, algorithmScript, idText)
            else:
                print "[FAILED] The mean AUROC was %.3f for %s and %s. The expected lower threshold is %.3f. {%s}" % (meanAUC, description, algorithmScript, lowerThreshold, idText)
                failedAlgorithms.add(algorithmScript)
        elif description.startswith("MediumSignal"):
            lowerThreshold = 0.6
            upperThreshold = 0.9
            if meanAUC >= lowerThreshold and meanAUC <= upperThreshold:
                print "[PASSED] The mean AUROC was %.3f for %s and %s. {%s}" % (meanAUC, description, algorithmScript, idText)
            else:
                print "[FAILED] The mean AUROC was %.3f for %s and %s. The expected lower threshold is %.3f. The expected upper threshold is %.3f. {%s}" % (meanAUC, description, algorithmScript, lowerThreshold, upperThreshold, idText)
                failedAlgorithms.add(algorithmScript)
        elif description.startswith("NoSignal"):
            upperThreshold = 0.6
            if meanAUC <= upperThreshold:
                print "[PASSED] The mean AUROC was %.3f for %s and %s. {%s}" % (meanAUC, description, algorithmScript, idText)
            else:
                print "[FAILED] The mean AUROC was %.3f for %s and %s. The expected upper threshold is %.3f. {%s}" % (meanAUC, description, algorithmScript, upperThreshold, idText)
                failedAlgorithms.add(algorithmScript)

print "\n[TEST SUMMARY]\n"
if len(failedAlgorithms) > 0:
    print "The following algorithm(s) failed at least once:"
    for algorithm in failedAlgorithms:
        print "  %s" % algorithm
    exit(1)
else:
    print "Tests passed!\n"
