import os, sys

paramOfInterest = sys.argv[1]
isRequired = sys.argv[2] == "TRUE"

default = None
if isRequired:
    userArgs = sys.argv[3:]
else:
    default = sys.argv[3]
    userArgs = sys.argv[4:]

values = []

wasFound = False
for i in range(len(userArgs)):
    if userArgs[i] == paramOfInterest:
        wasFound = True

        if i == (len(userArgs) - 1):
            print("ERROR: The {} argument was specified, but there was no accompanying value.".format(paramOfInterest))
            sys.exit(0)

        value = userArgs[i+1]
        if value.startswith("-"):
            print("ERROR: The {} argument was specified, but there was no accompanying value.".format(paramOfInterest))
            sys.exit(0)

        values.append(value)

if not wasFound:
    if isRequired:
        print("ERROR: No {} argument was specified. This argument is required.".format(paramOfInterest))
    else:
        print(default)

    sys.exit(0)

print(",".join(values))
