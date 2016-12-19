import sys

for line in sys.stdin:
    #if not line.upper().startswith("WARNING:"):
    if not " " in line:
        print line.rstrip()
    else:
        sys.stderr.write(line)
