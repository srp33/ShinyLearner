import sys

inFilePath = sys.argv[1]
findValue = sys.argv[2].decode('string-escape')
replaceValue = sys.argv[3].decode('string-escape')

if len(sys.argv) > 4:
    outFilePath = sys.argv[4]
else:
    outFilePath = inFilePath

def readTextFromFile(filePath):
    text = ""

    for line in file(filePath, 'rU'):
        text += line

    return text

def writeScalarToFile(x, filePath):
    outFile = open(filePath, 'w')
    outFile.write(x)
    outFile.close()

text = readTextFromFile(inFilePath)
text = text.replace(findValue, replaceValue)
writeScalarToFile(text, outFilePath)
