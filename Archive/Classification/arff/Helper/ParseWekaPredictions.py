import sys

classOptions = sys.argv[1].split(",")

predictionLines = []
haveReachedPredictions = False
for line in sys.stdin:
    if haveReachedPredictions:
        if line.strip() != "":
            predictionLines.append(line.strip())
    else:
        haveReachedPredictions = line.strip().startswith("inst#")

for line in predictionLines:
    lineItems = line.rstrip().replace("+", "").split(" ")
    lineItems = [x for x in lineItems if x != ""]

    predictionIndex = int(lineItems[2].split(":")[0]) - 1
    prediction = classOptions[predictionIndex]
    probabilities = [x.replace("*", "") for x in lineItems[3].split(",")]

    print "%s\t%s" % (prediction, "\t".join(probabilities))
