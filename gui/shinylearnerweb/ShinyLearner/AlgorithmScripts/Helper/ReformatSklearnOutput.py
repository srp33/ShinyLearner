import sys

# This seems to be a somewhat reasonable way to avoid printing warnings.
for line in sys.stdin:
    if " " not in line:
        print(line.rstrip())
    else:
        sys.stderr.write(line)
