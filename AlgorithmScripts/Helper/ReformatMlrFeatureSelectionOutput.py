import re
import sys

features = []

for line in sys.stdin:
    if re.match(r"^\d+\s+", line):
        features.append(re.sub(r"^\d+\s+", "", line.rstrip("\n")))

print(",".join(features))
