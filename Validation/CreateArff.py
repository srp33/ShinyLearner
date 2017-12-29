import os, sys, glob, gzip

inFilePath = sys.argv[1]
outFilePath = sys.argv[2]

classValues = []
inFile = gzip.open(inFilePath)
inFile.readline()
for line in inFile:
    classValues.append(line.decode().rstrip().split("\t")[-1])
inFile.close()

inFile = gzip.open(inFilePath)
features = inFile.readline().decode().strip().split("\t")

outFile = gzip.open(outFilePath, 'w')
outFile.write("@relation data\n\n".encode())

outFile.write("@attribute ID string\n".encode())
for feature in features[:-1]:
    outFile.write("@attribute {} numeric\n".format(feature).encode())
outFile.write("@attribute Class {{{}}}\n\n".format(",".join(sorted(list(set(classValues))))).encode())

outFile.write("@data\n".encode())

for line in inFile:
    lineItems = line.decode().rstrip().split("\t")
    outFile.write((",".join(lineItems) + "\n").encode())

outFile.close()
inFile.close()
