import os, sys

outFilePath = sys.argv[1]
inFilePaths = sys.argv[2:]

outFile = open(outFilePath, 'w')

headerWritten = False
for inFilePath in inFilePaths:
    inFile = open(inFilePath)

    headerLine = inFile.readline()
    if not headerWritten:
        outFile.write(headerLine)
        headerWritten = True

    for line in inFile:
        outFile.write(line)

    inFile.close()

outFile.close()
