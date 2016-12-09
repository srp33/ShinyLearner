import sys, gzip

inFilePath = sys.argv[1]
outFilePath = sys.argv[2]

inFile = gzip.open(inFilePath)
lines = [line for line in inFile]
inFile.close()

outFile = gzip.open(outFilePath, 'w')
for line in lines[:-1]:
    outFile.write(line)
outFile.close()
