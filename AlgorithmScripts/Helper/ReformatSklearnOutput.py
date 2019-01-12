import sys

classOptions = set(sys.argv[1].split(","))
verbose = sys.argv[2] == "true"

# This seems to be a somewhat reasonable way to avoid printing warnings.
for line in sys.stdin:
    #lineItems = line.rstrip("\n").split("\t")
    #if not lineItems[0] in classOptions:
    if " " in line:
        if verbose:
            sys.stderr.write(line)
    else:
        print(line.rstrip())
