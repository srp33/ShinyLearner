import os, sys, glob

logFilePaths = glob.glob(sys.argv[1])
expectedNumLogFiles = int(sys.argv[2])

if len(logFilePaths) != expectedNumLogFiles:
    print "An insufficient number of log files was found: %i" % len(logFilePaths)
    exit(1)

successLineCount = 0
failureOutput = ""
for logFilePath in logFilePaths:
    for line in file(logFilePath):
        if "Exception" in line or "[FAILED]" in line or ("Error" in line and "ErrorRate" not in line):
            failureOutput += "\n" + line
        elif "[PASSED]" in line:
            successLineCount += 1

print "\n*******************************************************\n"
if failureOutput == "":
    if successLineCount > 0:
        print "The build test log files look OK!"
    else:
        print "The log file contained no successful lines."
        exit(1)
else:
    print failureOutput
    print "At least one error occurred. Please address it!!!"
    exit(1)
print "\n*******************************************************\n"
