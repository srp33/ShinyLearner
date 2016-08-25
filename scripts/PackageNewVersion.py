import os, posix, shutil

versionFile = open("ML-Flex/Version.txt")
version = versionFile.readline().strip()
versionFile.close()

#tarGzFilePath = "ML-Flex_%s.tar.gz" % version
#posix.system("tar zcvf %s ML-Flex" % tarGzFilePath)
#shutil.copy(tarGzFilePath, "ML-Flex/" + tarGzFilePath)
