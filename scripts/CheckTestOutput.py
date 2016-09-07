import os, sys

logFilePath = sys.argv[1]

logInfo = "".join([line for line in file(logFilePath)])

if "[FAILED]" in logInfo:
    print "Failures occurred, so halting."
    sys.exit(1)
