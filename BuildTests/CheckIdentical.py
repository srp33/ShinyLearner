import os, sys, glob

inFilePath1 = sys.argv[1]
inFilePath2 = sys.argv[2]

inFile1 = open(inFilePath1)
inFile2 = open(inFilePath2)

inFile1.readline()
inFile2.readline()

misMatchCount = 0
for line1 in inFile1:
    line2 = inFile2.readline()
    if line1 != line2:
        print("[FAILED] Mismatch between {} and {}:".format(inFilePath1, inFilePath2))
        print("  {}".format(line1.rstrip()))
        print("  {}".format(line2.rstrip()))

        misMatchCount += 1
        if misMatchCount == 10:
            break

inFile2.close()
inFile1.close()

if misMatchCount > 0:
    sys.exit(1)
else:
    print("[SUCCESS] Current results match previous results")
