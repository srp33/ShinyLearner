import sys

# This seems to be a somewhat reasonable way to avoid printing warnings.
for line in sys.stdin:
    if line.startswith("INFO:") or "com.linkedin.paldb.impl" in line or line.startswith("Max offset length:") or line.startswith("Slot size:") or line.startswith("Key count:") or line.startswith("Index size:") or line.startswith("Data size:") or line.startswith("Created at:") or line.startswith("Format version:") or line.startswith("Number of memory mapped data buffers:"):
        continue

    print line.rstrip()
