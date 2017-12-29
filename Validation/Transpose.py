import os, sys, gzip
import numpy

inFilePath = sys.argv[1]
outFilePath = sys.argv[2]

def readMatrixFromFile(filePath):
    matrix = []

    inFile = gzip.open(filePath)
    for line in inFile:
        #matrix.append(line.decode().rstrip().split("\t"))
        matrix.append(line.rstrip().split("\t"))

    return matrix

def writeMatrixToFile(x, filePath, writeMode='w'):
    outFile = gzip.open(filePath, writeMode)
    writeMatrixToOpenFile(x, outFile)
    outFile.close()

def writeMatrixToOpenFile(x, outFile):
    for y in x:
        outFile.write("\t".join([str(z) for z in y]) + "\n")

def transposeMatrix(x):
    transposed = zip(*x)
    #transposed = numpy.transpose(x)

    for i in range(len(transposed)):
        transposed[i] = list(transposed[i])

    return transposed

data = readMatrixFromFile(inFilePath)
writeMatrixToFile(transposeMatrix(data), outFilePath)
