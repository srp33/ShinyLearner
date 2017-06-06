import os, sys

paramOfInterest = sys.argv[1]
isRequired = sys.argv[2] == "TRUE"
valueIsRequired = sys.argv[3] == "TRUE"
userArgs = sys.argv[4:]

values = []

wasFound = False
for i in range(len(userArgs)):
    if userArgs[i] == paramOfInterest:
        wasFound = True

        if not valueIsRequired:
            continue

        if i == (len(userArgs) - 1):
            print "ERROR: The %s argument was specified, but there was no accompanying value." % paramOfInterest
            sys.exit(0)

        value = userArgs[i+1]
        if value.startswith("-"):
            print "ERROR: The %s argument was specified, but there was no accompanying value." % paramOfInterest
            sys.exit(0)

        values.append(value)

if isRequired and not wasFound:
    print "ERROR: No %s argument was specified. This argument is required." % paramOfInterest
    sys.exit(0)

if valueIsRequired and len(values) == 0:
    print "ERROR: No %s argument value was specified. A value is required for this argument." % paramOfInterest
    sys.exit(0)

if not valueIsRequired:
    if wasFound:
        print paramOfInterest
else:
    print ",".join(values)
