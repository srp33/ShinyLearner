import sys

classOptions = set(sys.argv[1].split(","))

for line in sys.stdin:
    lineItems = line.rstrip().split("\t")

    if len(lineItems) < 2:
        continue

    if lineItems[1] in classOptions:
        print "%s\t%s\t%s" % (lineItems[0], lineItems[1], "\t".join(["%.9f" % float(x) for x in lineItems[2:]]))
