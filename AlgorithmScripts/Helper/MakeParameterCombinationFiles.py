import os, sys
import itertools as it

outFilePath = sys.argv[1]

parameterDict = {}

for parameter in sys.argv[2:]:
    parameterName = parameter.split("=")[0]
    parameterOptions = parameter.split("=")[1].split(",")

    parameterDict[parameterName] = parameterOptions

parameterNames = sorted(parameterDict.keys())
outLines = [parameterNames]

combinations = [dict(zip(parameterNames, prod)) for prod in it.product(*(parameterDict[varName] for varName in parameterNames))]

for combo in combinations:
    outLines.append([combo[parameterName] for parameterName in parameterNames])

outFile = open(outFilePath, 'w')
for outLine in outLines:
    outFile.write("\t".join(outLine) + "\n")
outFile.close()
