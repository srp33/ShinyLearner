import os, sys

templateFilePath = sys.argv[1]
versionFilePath = sys.argv[2]
increment = sys.argv[3] == "True"
outFilePath = sys.argv[4]

version = int([line.rstrip() for line in file(versionFilePath)][0])

if increment:
    version = version + 1

outFile = open(outFilePath, 'w')
for line in file(templateFilePath):
    line = line.replace("{version}", str(version))
    outFile.write(line)
outFile.close()

versionFile = open(versionFilePath, 'w')
versionFile.write("%i" % version)
versionFile.close()
