import os, sys

logFilePath = sys.argv[1]
message = sys.argv[2]

success = False
for line in file(logFilePath):
    if message in line:
        print "[PASSED] This message (\"" + message + "\") was expected to be found in " + logFilePath + "."
        success = True
        break

if not success:
    print "[FAILED] This message (\"" + message + "\") was expected to be found in " + logFilePath + "."
