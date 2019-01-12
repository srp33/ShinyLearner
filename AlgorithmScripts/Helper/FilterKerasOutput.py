import sys

classOptions = set(sys.argv[1].split(","))
verbose = sys.argv[2] == "true"

# This seems to be a somewhat reasonable way to avoid printing warnings.

lines = [line for line in sys.stdin if line.strip() != ""]

# Sometimes keras prints a message indicating that it couldn't access a tensorflow session
#   but still executes successfully. We are going to remove that from the output.
line_indices_to_ignore = set()
for i in range(len(lines)):
    if lines[i].startswith("Exception ignored"):
        line_indices_to_ignore.add(i)
        line_indices_to_ignore.add(i + 1)
        line_indices_to_ignore.add(i + 2)
        line_indices_to_ignore.add(i + 3)

    if "Your CPU supports instructions that this TensorFlow binary was not compiled to use" in lines[i]:
        line_indices_to_ignore.add(i)

errorText = ""

line_index_generator = range(len(lines))

for i in line_index_generator:
    if i in line_indices_to_ignore:
        continue

    line = lines[i]
    lineItems = line.rstrip("\n").split("\t")

    if len(lineItems) < 2:
        errorText += line
        continue

    if not lineItems[0] in classOptions:
        errorText += line
        continue

    print(line.rstrip())

if errorText != "" and verbose:
    print(errorText)
