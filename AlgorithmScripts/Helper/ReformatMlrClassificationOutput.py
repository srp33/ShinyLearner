import sys

sys.setdefaultencoding('ascii')

classOptions = set(sys.argv[1].split(","))
verbose = sys.argv[2] == "true"

for line in sys.stdin:
    lineItems = line.split("\t")
    if lineItems[0] in classOptions:
        print(line.rstrip())
    else:
        if verbose:
            sys.stderr.write(line)
