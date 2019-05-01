import sys

print(",".join([sys.argv[2] + x for x in sys.argv[1].split(",")]))
