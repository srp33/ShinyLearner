import os, sys

taskType = sys.argv[1]
validationType = sys.argv[2]
description = sys.argv[3]
metricFilePath = sys.argv[4]
algorithmColumnName = sys.argv[5]
expectedNumAlgorithms = int(sys.argv[6])
expectedNumEnsemble = int(sys.argv[7])

if not os.path.exists(metricFilePath):
    print("[FAILED] No metric file found!")
    exit(1)

successfulAlgorithms = set()
failedAlgorithms = []
failedAlgorithmOutput = ""

metricFile = open(metricFilePath)
metricData = [line.rstrip().split("\t") for line in metricFile]
metricFile.close()

headerItems = metricData.pop(0)
metricNameIndex = headerItems.index("Metric")
valueIndex = headerItems.index("Value")
algorithmIndex = headerItems.index(algorithmColumnName)

uniqueAlgorithms = list(set([row[algorithmIndex] for row in metricData]))

if len(uniqueAlgorithms) == 0:
    print("[FAILED] No algorithm scripts could be found.")
    exit(1)

actualNumAlgorithms = len([x for x in uniqueAlgorithms if not x.startswith("Ensemble")])
actualNumEnsemble = len([x for x in uniqueAlgorithms if x.startswith("Ensemble")])

if actualNumAlgorithms != expectedNumAlgorithms:
    print("[FAILED] The number of classification algorithms in {} [{}] does not match the expected number [{}].".format(metricFilePath, actualNumAlgorithms, expectedNumAlgorithms))
    exit(1)

if actualNumEnsemble != expectedNumEnsemble:
    print("[FAILED] The number of ensemble algorithms in {} [{}] does not match the expected number [{}].".format(metricFilePath, actualNumEnsemble, expectedNumEnsemble))
    exit(1)

for algorithm in uniqueAlgorithms:
    if "ZeroR" in algorithm:
        continue
    if "demo" in algorithm:
        continue

    idText = "{} - {} - {} - {}".format(taskType, validationType, metricFilePath, algorithm)

    aucValues = [float(row[valueIndex]) for row in metricData if row[algorithmIndex] == algorithm and row[metricNameIndex] == "AUROC"]
    meanAUC = sum(aucValues) / float(len(aucValues))

    if description.startswith("StrongSignal"):
        lowerThreshold = 0.75
        if meanAUC >= lowerThreshold:
            print("[PASSED] The mean AUROC was {:.3f} for {} and {}. ({})".format(meanAUC, description, algorithm, idText))
            successfulAlgorithms.add(algorithm)
        else:
            error = "[FAILED] The mean AUROC was {:.3f} for {} and {}. The expected lower threshold is {:.3f}. ({})".format(meanAUC, description, algorithm, lowerThreshold, idText)
            print(error)
            failedAlgorithms.append(algorithm)
            failedAlgorithmOutput += error + "\n"
    elif description.startswith("NoSignal"):
        upperThreshold = 0.75
        if meanAUC <= upperThreshold:
            print("[PASSED] The mean AUROC was {:.3f} for {} and {}. ({})".format(meanAUC, description, algorithm, idText))
            successfulAlgorithms.add(algorithm)
        else:
            error = "[FAILED] The mean AUROC was {:.3f} for {} and {}. The expected upper threshold is {:.3f}. ({})".format(meanAUC, description, algorithm, upperThreshold, idText)
            print(error)
            failedAlgorithms.append(algorithm)
            failedAlgorithmOutput += error + "\n"

print("\n[TEST SUMMARY]\n")

if len(successfulAlgorithms) == 0:
    print("[FAILED] No algorithms successfully passed any of the tests.")
    exit(1)

if len(failedAlgorithms) > 0:
    print("The following algorithm(s) failed at least once:")
    for algorithm in failedAlgorithms:
        print("  {}".format(algorithm))
    print("\n" + failedAlgorithmOutput)
    exit(1)
else:
    print("Tests passed!\n")
