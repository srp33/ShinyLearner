import os, sys, glob

inFilePath1 = sys.argv[1]
inFilePath2 = sys.argv[2]

inFile1 = open(inFilePath1)
inFile2 = open(inFilePath2)

inFile1.readline()
inFile2.readline()

for line1 in inFile1:
    line2 = inFile2.readline()
    if line1 != line2:
        print "[FAILED] Files are not identical. Printing first non-match."
        print "File 1: %s" % inFilePath1
        print line1.rstrip()
        print "File 2: %s" % inFilePath2
        print line2.rstrip()

        inFile2.close()
        inFile1.close()
        sys.exit(1)

inFile2.close()
inFile1.close()

#if not areIdentical:
#    print "[FAILED] Files are not identical:"
#    print "  %s" % inFilePath1
#    print "  %s" % inFilePath2
#    print "  ======================================"
#
#
#    inFile1 = open(inFilePath1)
#    inFile2 = open(inFilePath2)
#
#    for line1 in inFile1:
#        line2 = inFile2.readline()
#
#        if line1 != line2:
#            print "  %s:" % inFilePath1
#            print "    %s" % line1
#            print "  %s:" % inFilePath2
#            print "    %s" % line2
#
#    inFile1.close()
#    inFile2.close()
#    print "  ======================================"
#
#    sys.exit(1)
