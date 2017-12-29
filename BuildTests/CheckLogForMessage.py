import os, sys

logFilePath = sys.argv[1]
message = sys.argv[2]

success = False
logFile = open(logFilePath)
for line in logFile:
    if message in line:
        print("[PASSED] This message (\"" + message + "\") was expected to be found in " + logFilePath + ".")
        success = True
        break
logFile.close()

if not success:
    print("[FAILED] This message (\"" + message + "\") was expected to be found in " + logFilePath + " but it was not found.")
