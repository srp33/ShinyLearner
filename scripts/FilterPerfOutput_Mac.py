import sys

inFilePath = sys.argv[1]
outFilePath = sys.argv[2]

outFile = open(outFilePath, 'w')

inFile = open(inFilePath)
for line in inFile:
    if line.startswith("Mach Virtual Memory Statistics"):
        continue

    if line.strip().startswith("free"):
        continue

    line = ' '.join(line.split())
    lineItems = line.split(" ")

    mem = float(int(lineItems[0]) + int(lineItems[3]))
    mem = mem / 256000

    outFile.write("{:.3f}\n".format(mem))

inFile.close()
outFile.close()

#  cat /tmp/vm_stat_raw | awk 'NR>2 {gsub("K","000");print ($1+$4)/256000}' > $outFile
