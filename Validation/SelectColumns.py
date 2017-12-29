import os, sys, glob, gzip

def parseColumnIndices(entries, lastIndex):
    indices = []

    for entry in entries:
        if entry == "last":
            indices.append(lastIndex - 1)
        else:
            if entry.find("to") > -1:
                entryValues = entry.split("to")
                start = int(entryValues[0])

                if entryValues[1] == "last":
                    stop = lastIndex
                elif entryValues[1].startswith("-"):
                    stop = lastIndex + int(entryValues[1]) + 1
                else:
                    stop = int(entryValues[1]) + 1

                indices.extend(range(start, stop))
            else:
                indices.append(int(entry))

    return indices

inFilePath = sys.argv[1]
columnIndexInput = sys.argv[2]
outFilePath = sys.argv[3]

lineCount = 0
outFile = gzip.open(outFilePath, 'w')
out = ""
columnIndices = None

inFile = gzip.open(inFilePath)
for line in inFile:
    lineCount += 1
    lineItems = line.decode().rstrip().split("\t")

    if columnIndices is None:
        columnIndices = parseColumnIndices(columnIndexInput.split(","), len(lineItems))

    try:
        outItems = [lineItems[i] for i in columnIndices if len(lineItems) > i]
    except:
        print(sys.exc_info())
        print(lineItems)
        exit()

    out += "\t".join(outItems) + "\n"

    if lineCount % 100000 == 0:
        print(lineCount)
        outFile.write(out.encode())
        out = ""

outFile.write(out.encode())
outFile.close()
inFile.close()
