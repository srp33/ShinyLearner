import sys

classOptions = set(sys.argv[1].split(","))

for line in sys.stdin:
    lineItems = line.rstrip().split("\t")
    if lineItems[0] in classOptions:
        print "%s\t%s" % (lineItems[0], "\t".join(["%.9f" % float(x) for x in lineItems[1:]]))
