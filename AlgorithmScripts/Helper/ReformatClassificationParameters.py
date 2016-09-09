import sys

inputParams = sys.stdin.readline().rstrip()

if " -- " not in inputParams:
    print inputParams
else:
    partA = inputParams.split(" -- ")[0]
    partB = " -t " + inputParams.split(" -t ")[1]
    partC = " -- " + inputParams.split(" -- ")[1].split(" -t ")[0]

    print partA + partB + partC
