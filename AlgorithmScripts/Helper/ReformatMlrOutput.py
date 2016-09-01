import sys

for line in sys.stdin:
    if not line.upper().startswith("WARNING:"):
        print line.rstrip()
