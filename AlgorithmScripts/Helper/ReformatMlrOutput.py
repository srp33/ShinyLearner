import sys

classOptions = set(sys.argv[1].split(","))

for line in sys.stdin:
    #if not line.upper().startswith("WARNING:"):
    #if not " " in line:
    lineItems = line.split("\t")
    if lineItems[0] in classOptions:
        print line.rstrip()
