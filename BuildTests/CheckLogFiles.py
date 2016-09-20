import os, sys, glob

logFilePaths = glob.glob(sys.argv[1])
expectedNumLogFiles = int(sys.argv[2])

if len(logFilePaths) != expectedNumLogFiles:
    print "An insufficient number of log files was found: %i" % len(logFilePaths)
    exit(1)

failureOutput = ""
for logFilePath in logFilePaths:
    for line in file(logFilePath):
        if "Exception" in line or "Error" in line or "[FAILED]" in line:
            failureOutput += "\n" + line

if failureOutput != "":
    print "*******************************************************"
    print failureOutput
    print "At least one error occurred. Please address it!!!"
    print "*******************************************************"
    exit(1)
