import os, sys, glob, gzip

inFilePath = sys.argv[1]
outFilePath = sys.argv[2]

classValues = []
inFile = gzip.open(inFilePath)
inFile.readline()
for line in inFile:
    classValues.append(line.rstrip().split("\t")[-1])
inFile.close()

inFile = gzip.open(inFilePath)
features = inFile.readline().strip().split("\t")

outFile = gzip.open(outFilePath, 'w')
outFile.write("@relation data\n\n")

outFile.write("@attribute ID string\n")
for feature in features[:-1]:
    outFile.write("@attribute %s numeric\n" % feature)
outFile.write("@attribute Class {%s}\n\n" % ",".join(sorted(list(set(classValues)))))

outFile.write("@data\n")

for line in inFile:
    lineItems = line.rstrip().split("\t")
    outFile.write(",".join(lineItems) + "\n")

outFile.close()
inFile.close()
