import sys

verbose = sys.argv[1] == "true"

for line in sys.stdin:
    #if not line.upper().startswith("WARNING:"):
    if not " " in line:
        print(line.rstrip())
    else:
        if verbose:
            sys.stderr.write(line)
