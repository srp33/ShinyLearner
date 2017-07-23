import os, sys, glob

trainTestFilePath = sys.argv[1]
classifAlgosRaw = sys.argv[2]
outFilePath = sys.argv[3]
verbose = sys.argv[4] == "true"

def smartPrint(output):
    if verbose:
        print(output)

smartPrint("pwd:")
smartPrint(os.path.dirname(os.path.realpath(__file__)))

classifAlgos = set()
for x in classifAlgosRaw.split(","):

    smartPrint("x:" + x)
    for y in glob.glob(x):
        smartPrint("y:" + y)
        if os.path.isdir(y):
            smartPrint("isdir")
            for z in glob.glob(y.rstrip("/") + "/*"):
                smartPrint("zz:" + z)
                classifAlgos.add(z)
        elif y.endswith(".list"):
            smartPrint("islist")
            for line in file(y):
                classifAlgos.add(line.rstrip())
        else:
            smartPrint("other")
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
