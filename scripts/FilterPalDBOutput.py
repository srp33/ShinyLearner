import sys

# This seems to be a somewhat reasonable way to avoid printing warnings.
for line in sys.stdin:
    if not line.startswith("INFO:") and not "com.linkedin.paldb.impl.StorageWriter" in line:
        print line.rstrip()
