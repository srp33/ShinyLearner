import os, sys, shutil
import itertools as it

def createScript(algorithmType, packagePath, templateFilePath, shortAlgName, algFileName, algClass, instantiation, paramDict):
    scriptDir = "../{}/{}/{}".format(algorithmType, packagePath, shortAlgName)
    if not os.path.exists(scriptDir):
        os.makedirs(scriptDir, exist_ok=True)

    destFilePath = "{}/{}".format(scriptDir, algFileName)

    if os.path.exists(destFilePath):
        print("File already exists at {}".format(destFilePath))
        sys.exit(1)

    print("Saving to {}".format(destFilePath))

    # Copy the file first to preserve permissions
    shutil.copy(templateFilePath, destFilePath)

    with open(destFilePath) as templateFile:
        template = templateFile.read()

        if algClass != None:
            template = template.replace("{algorithmClass}", algClass)

        algInstantiation = replaceTokens(instantiation, paramDict, shortAlgName)
        template = template.replace("{algorithmInstantiation}", algInstantiation)

    with open(destFilePath, 'w') as destFile:
        destFile.write(template)

    if not os.path.exists(destFilePath):
        print("Error occurred when saving to {}.".format(destFilePath))
        sys.exit(1)

def replaceTokens(instantiation, paramDict, shortAlgName):
    for key, value in paramDict.items():
        if "{" + key + "}" not in instantiation:
            print("A key of {} was not found in the algorithm template for {}.".format(key, shortAlgName))
            sys.exit(1)
        instantiation = instantiation.replace("{" + key + "}", str(value))

    return instantiation

def createScripts(algorithmType, packagePath, templateFilePath, shortAlgName, algClass, instantiation, paramDict, summaryDict, *ignoreDicts):
    defaultParamComboDict = parseDefaultParams(paramDict)

    for paramComboDict in parseNonDefaultParamCombos(paramDict):
        if ignore(paramComboDict, ignoreDicts):
            #print("Ignoring:")
            #print(paramComboDict)
            continue

        if paramComboDict == defaultParamComboDict:
            prefix = "default"
        else:
            prefix = "alt"

        paramName = buildParamName(prefix, paramDict, paramComboDict)
        createScript(algorithmType, packagePath, templateFilePath, shortAlgName, paramName, algClass, instantiation, paramComboDict)

        summaryDict[shortAlgName] = summaryDict.setdefault(shortAlgName, 0) + 1

def ignore(comboDict, ignoreDicts):
    if len(ignoreDicts) == 0:
        return False

    for ignoreDict in ignoreDicts:
        for ignoreKey, ignoreValue in ignoreDict.items():
            if ignoreKey not in comboDict:
                print("Ignore key [{}] does not align with param dict.".format(ignoreKey))
                sys.exit(1)

        comboIntersectDict = {x:comboDict[x] for x in comboDict if x in ignoreDict}

        if comboIntersectDict == ignoreDict:
            return True

    return False

def parseDefaultParams(paramDict):
    defaultParamDict = {}

    for key, value in paramDict.items():
        defaultParamDict[key] = value[0]

    return defaultParamDict

def parseNonDefaultParamCombos(paramDict):
    parameterNames = sorted(paramDict.keys())
    return [dict(zip(parameterNames, prod)) for prod in it.product(*(paramDict[varName] for varName in parameterNames))]

def buildParamName(prefix, paramDict, paramComboDict):
    paramName = prefix + "_"

    for key in sorted(paramComboDict.keys()):
        if len(paramDict[key]) > 1:
            value = str(paramComboDict[key])

            # Some parameters are complex, just get the first part, splitting by spaces
            if value.startswith("weka."):
                value = value.split(" ")[0]

            paramName += "_" + key + "=" + replaceSpecialChars(value)

    paramName = paramName.strip("_")

    if len(paramName) > 255:
        print("The name of the parameter file is too long: {}.".format(paramName))
        sys.exit(1)

    return paramName

def replaceSpecialChars(value):
    return value.replace(";", "_").replace(" ", "_").replace("()", "").replace("(", "").replace(")", "").replace(",", "").replace("/", "").replace("'", "").replace("\"", "")
