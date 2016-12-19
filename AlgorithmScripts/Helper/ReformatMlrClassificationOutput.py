import sys

classOptions = set(sys.argv[1].split(","))

for line in sys.stdin:
    lineItems = line.split("\t")
    if lineItems[0] in classOptions:
        print line.rstrip()
    else:
        sys.stderr.write(line)
