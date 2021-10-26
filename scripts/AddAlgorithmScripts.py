import os, sys, glob

trainTestFilePath = sys.argv[1]
classifAlgosRaw = sys.argv[2]
outFilePath = sys.argv[3]
verbose = sys.argv[4] == "true"

def smartPrint(output):
    if verbose:
        print(output)

#smartPrint("pwd: " + os.getcwd())

classifAlgos = set()
for x in classifAlgosRaw.split(","):
#    smartPrint("x: " + x)
    for y in glob.glob(x):
#        smartPrint("y: " + y)
        if os.path.isdir(y):
#            smartPrint("isdir")
            for z in glob.glob(y.rstrip("/") + "/*"):
#                smartPrint("zz: " + z)
                classifAlgos.add(z)
        elif y.endswith(".list"):
#            smartPrint("islist")
            yFile = open(y)
            for line in yFile:
                classifAlgos.add(line.rstrip())
            yFile.close()
        else:
#            smartPrint("other")
            classifAlgos.add(y)

classifAlgos = sorted(list(classifAlgos))

#for classifAlgo in classifAlgos:
#    smartPrint("classifAlgo: " + classifAlgo)

outLines = []
#smartPrint("trainTestFile:")
trainTestFile = open(trainTestFilePath)
for line in trainTestFile:
#    smartPrint("ttf: " + line)
    for classifAlgo in classifAlgos:
#        smartPrint("ttfca: " + classifAlgo)
        outLines.append(line.rstrip() + "\t" + classifAlgo + "\n")
trainTestFile.close()

if len(outLines) == 0:
    print("No algorithm scripts matched the input path(s) specified: {}".format(classifAlgosRaw))
    exit(1)

outFile = open(outFilePath, 'w')
for outLine in outLines:
    outFile.write(outLine)
outFile.close()
