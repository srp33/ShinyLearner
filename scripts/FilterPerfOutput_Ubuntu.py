import sys

inFilePath = sys.argv[1]
outFilePath = sys.argv[2]

outFile = open(outFilePath, 'w')

#procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
# r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
# 1  0  91148 127044320 1002212 255306560    0    0    17    26    0    0  1  0 99  0  0

inFile = open(inFilePath)
for line in inFile:
    if line.startswith("procs"):
        continue

    if line.strip().startswith("r"):
        continue

    line = ' '.join(line.split())
    lineItems = line.split(" ")

    mem = float(lineItems[3])
    mem = mem / (1024.0 * 1024.0)

    outFile.write("{:.3f}\n".format(mem))

inFile.close()
outFile.close()
