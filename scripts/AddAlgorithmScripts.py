import os, sys, glob

trainTestFilePath = sys.argv[1]
classifAlgosRaw = sys.argv[2]
outFilePath = sys.argv[3]

classifAlgos = set()
for x in classifAlgosRaw.split(","):
    for y in glob.glob(x):
        if os.path.isdir(y):
            for z in glob.glob(y.rstrip("/") + "/*"):
                classifAlgos.add(z)
        elif y.endswith(".list"):
            for line in file(y):
                classifAlgos.add(line.rstrip())
        else:
            classifAlgos.add(y)

classifAlgos = sorted(list(classifAlgos))

outLines = []
for line in file(trainTestFilePath):
    for classifAlgo in classifAlgos:
        outLines.append(line.rstrip() + "\t" + classifAlgo + "\n")

if len(outLines) == 0:
    print "No algorithm scripts matched the input path(s) specified: %s" % classifAlgosRaw
    exit(1)

outFile = open(outFilePath, 'w')
for outLine in outLines:
    outFile.write(outLine)
outFile.close()
