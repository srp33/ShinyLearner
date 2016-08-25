import os, sys, glob

inFilePath1 = sys.argv[1]
inFilePath2 = sys.argv[2]

inFile1 = open(inFilePath1)
inFile2 = open(inFilePath2)

inFile1.readline()
inFile2.readline()

areIdentical = True

for line1 in inFile1:
    line2 = inFile2.readline()
    if line1 != line2:
        areIdentical = False
        break

inFile2.close()
inFile1.close()

if areIdentical:
    print "[PASSED]"
    print "  %s" % inFilePath1
    print "  %s" % inFilePath2
else:
    print "[FAILED]"
    print "  %s" % inFilePath1
    print "  %s" % inFilePath2
    print "  ======================================"

    inFile1 = open(inFilePath1)
    inFile2 = open(inFilePath2)

    for line1 in inFile1:
        line2 = inFile2.readline()

        if line1 != line2:
            print "  %s:" % inFilePath1
            print "    %s" % line1
            print "  %s:" % inFilePath2
            print "    %s" % line2

    inFile1.close()
    inFile2.close()

    sys.exit(1)
