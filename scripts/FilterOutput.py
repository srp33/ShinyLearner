import sys

verbose = sys.argv[1] == "true"

for line in sys.stdin:
    line = line.strip()
    if not verbose and line.startswith("INFO:") or "com.linkedin.paldb.impl" in line or line.startswith("Max offset length:") or line.startswith("Slot size:") or line.startswith("Key count") or line.startswith("Index size:") or line.startswith("Data size:") or line.startswith("Created at:") or line.startswith("Format version:") or line.startswith("Number of memory mapped data buffers:") or line.startswith("Parsed with column specification") or line == "cols(" or line == ")" or "col_character()" in line or "col_integer()" in line or line.startswith("Joining, by ="):
        continue

    print line.rstrip()
