import sys

inFilePath = sys.argv[1]
outFilePath = sys.argv[2]

attributes = []
dataLines = []

with open(inFilePath) as inFile:
    for line in inFile:
        line = line.strip()

        if len(line) == 0:
            continue

        if line.startswith("%"):
            continue

        if line.lower().startswith("@relation") or line.lower().startswith("@data"):
            continue

        if line.lower().startswith("@attribute"):
            attribute = line.lower().replace("@attribute ", "").replace(" real", "").replace(" integer", "").replace("'", "")

            if "{" in attribute:
                attribute = attribute.split(" {")[0]

            attribute = attribute.replace(" ", "_")
            attributes.append(attribute)
        else:
            dataLines.append(line.replace("'", "").replace(" ", "_").replace("-", "_"))

attributes[-1] = "Class"

outData = []
for line in dataLines:
    outData.append(line.split(","))

# Identify attributes with missing values
missingDict = {}
for i in range(len(attributes)):
    for row in outData:
        if row[i] == "?":
            if i not in missingDict:
                missingDict[i] = 1
            else:
                missingDict[i] += 1

if attributes.index("Class") in missingDict:
    print("Missing class values.")
    sys.exit(1)

if len(attributes) - len(missingDict) < 5:
    print("Too many missing values")
    sys.exit(1)

modOutData = []
for row in outData:
    modOutData.append([row[i] for i in range(len(attributes)) if i not in missingDict])

attributes = [attributes[i] for i in range(len(attributes)) if i not in missingDict]

with open(outFilePath, 'w') as outFile:
    outFile.write("\t".join(["ID"] + attributes) + "\n")

    sampleNum = 0
    for row in modOutData:
        sampleNum += 1
        outFile.write("\t".join(["Instance" + str(sampleNum)] + row) + "\n")
