import os, sys

templateFilePath = sys.argv[1]
versionFilePath = sys.argv[2]
increment = sys.argv[3] == "True"
outFilePath = sys.argv[4]

versionFile = open(versionFilePath)
version = int([line.rstrip() for line in versionFile][0])
versionFile.close()

if increment:
    version = version + 1

templateFile = open(templateFilePath)
template = templateFile.read().replace("{version}", str(version))

outFile = open(outFilePath, 'w')
outFile.write(template)
outFile.close()

versionFile = open(versionFilePath, 'w')
versionFile.write("{}".format(version))
versionFile.close()
