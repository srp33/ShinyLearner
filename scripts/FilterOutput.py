import sys

verbose = sys.argv[1] == "true"

if verbose:
    for line in sys.stdin:
        print line.strip()
        sys.stdout.flush()
        sys.stderr.flush()
else:
    for line in sys.stdin:
        line = line.strip()

        #if line.startswith("INFO:") or "com.linkedin.paldb.impl" in line or line.startswith("Max offset length:") or line.startswith("Slot size:") or line.startswith("Key count") or line.startswith("Index size:") or line.startswith("Data size:") or line.startswith("Created at:") or line.startswith("Format version:") or line.startswith("Number of memory mapped data buffers:") or line.startswith("Parsed with column specification") or line == "cols(" or line == ")" or "col_character()" in line or "col_integer()" in line or line.startswith("Joining, by =") or line.startswith("Number of keys:"):
        #if line.startswith("INFO:"):
        #    continue

        print line
        sys.stdout.flush()
        sys.stderr.flush()
