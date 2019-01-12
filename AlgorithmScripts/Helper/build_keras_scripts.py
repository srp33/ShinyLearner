import os, sys
from build_scripts_helper import *

showStats = sys.argv[1] == "True"

summaryDict = {}

#############################################################
# Meta options
#############################################################

packagePath = "tsv/keras"

#############################################################
# Classifiers
#############################################################

dnn = "{model_type};{layers};{dropout};{regularization};{batch_norm};{epochs}"
createScripts("Classification", packagePath, "keras_c_generic_template", "dnn", None, dnn, {"model_type": ["dnn"], "layers": ["16,16"], "dropout": ["0.5"], "regularization": ["0.1"], "batch_norm": ["true"], "epochs": ["100"]}, summaryDict)

snn = "{model_type};{layers};{dropout};{regularization};{batch_norm};{epochs}"
createScripts("Classification", packagePath, "keras_c_generic_template", "snn", None, snn, {"model_type": ["snn"], "layers": ["16,16"], "dropout": ["0.2"], "regularization": ["0.1"], "batch_norm": ["false"], "epochs": ["100"]}, summaryDict)

resnet = "{layer_width};{layers};{dropout};{regularization};{activation};{learning_rate};{epochs}"
createScripts("Classification", packagePath, "keras_c_resnet_template", "resnet", None, resnet, {"layer_width": ["16"], "layers": ["50"], "dropout": ["0.5"], "regularization": ["0.01"], "activation": ["selu"], "learning_rate": ["0.001"], "epochs": ["500"]}, summaryDict)

if showStats:
    print("#######################################")
    for key, value in sorted(summaryDict.items()):
        print(key, value)
    print("#######################################")
    print("Total: {}".format(sum(summaryDict.values())))
    print("#######################################")
