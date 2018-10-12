import sys

inputParams = sys.stdin.readline().rstrip()

if " -- " not in inputParams:
    print(inputParams)
else:
    partA = inputParams.split(" -- ")[0]
    partB = " -i " + inputParams.split(" -i ")[1]
    partC = " -- " + inputParams.split(" -- ")[1].split(" -s ")[0]
    partD = " -s " + inputParams.split(" -s ")[1].split(" -i ")[0]

    print(partA + partD + partB + partC)
