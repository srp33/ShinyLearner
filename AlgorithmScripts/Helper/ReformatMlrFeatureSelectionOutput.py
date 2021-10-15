import sys

verbose = sys.argv[1] == "true"

for line in sys.stdin:
    if line.startswith('c("'):
        features = line.rstrip("\n").replace('c("', '').replace(")", "").split(", ")
        features = [x.replace('"', '') for x in features]
        print(",".join(features).rstrip(","))

#        if verbose:
#            sys.stderr.write(line)
