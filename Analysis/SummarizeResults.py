import sys, glob

inFilePattern = sys.argv[1]
outFilePath = sys.argv[2]

outLines = []

for inFilePath in glob.glob(inFilePattern):
    with open(inFilePath) as inFile:
        headerLine = inFile.readline()

        if len(outLines) == 0:
            outLines.append(headerLine)

        for line in inFile:
            lineItems = line.rstrip("\n").split("\t")
            if lineItems[-2] == "AUROC":
                lineItems[0] = lineItems[0].replace("postoperative.patient.data", "Post-operative")
                lineItems[0] = lineItems[0].replace("sick", "Thyroid")
                lineItems[0] = lineItems[0].replace("breast.cancer", "Breast cancer")
                lineItems[0] = lineItems[0].replace("ecoli", "E. coli")
                lineItems[0] = lineItems[0].replace("mushroom", "Mushroom")
                lineItems[2] = lineItems[2].replace("AlgorithmScripts/Classification/arff/weka/", "")
                lineItems[2] = lineItems[2].replace("/default", "")

                if "Ensemble_Majority_Vote" not in line:
                    outLines.append("\t".join(lineItems) + "\n")

with open(outFilePath, 'w') as outFile:
    for line in outLines:
        outFile.write(line)
