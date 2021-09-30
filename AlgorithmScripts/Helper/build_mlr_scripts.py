import os, sys
from build_scripts_helper import *

showStats = sys.argv[1] == "True"

summaryDict = {}

#################################################################
# Meta options
#################################################################

packagePath = "tsv/mlr"

cOptions = [1.0, 0.1, 10.0, 100.0]
nodeSizeOptions = [1, 3, 5]

#################################################################
# Classification
#################################################################

## Focused on algorithms that support probabilistic predictions, multiclass and numerical + factor values. Some have been excluded because they don't work.

#boosting = "'classif.boosting', boos={boos}, mfinal={mfinal}, coeflearn='{coeflearn}'"
#createScripts("Classification", packagePath, "mlr_c_template", "boosting", None, boosting, {"boos": ["TRUE", "FALSE"], "mfinal": [100, 500], "coeflearn": ["Breiman", "Freund"]}, summaryDict)

C50 = "'classif.C50', subset = {subset}, winnow = {winnow}, noGlobalPruning = {noGlobalPruning}, CF = {CF}, minCases = {minCases}, fuzzyThreshold = {fuzzyThreshold}, sample = {sample}, earlyStopping = {earlyStopping}"
createScripts("Classification", packagePath, "mlr_c_template", "C50", None, C50, {"subset": ["FALSE", "TRUE"], "winnow": ["FALSE", "TRUE"], "noGlobalPruning": ["FALSE", "TRUE"], "CF": [0.25], "minCases": [2], "fuzzyThreshold": ["FALSE", "TRUE"], "sample": [0], "earlyStopping": ["TRUE", "FALSE"]}, summaryDict)

ctree = "'classif.ctree', teststat = '{teststat}', testtype = '{testtype}', mincriterion = {mincriterion}, minsplit = {minsplit}, minbucket = {minbucket}, stump = {stump}, nresample = {nresample}"
createScripts("Classification", packagePath, "mlr_c_template", "ctree", None, ctree, {"teststat": ['quad', 'max'], "testtype": ['Teststatistic'], "mincriterion": [0.95], "minsplit": [20], "minbucket": [7], "stump": ["FALSE", "TRUE"], "nresample": [9999]}, summaryDict)

earth = "'classif.earth', degree={degree}, newvar.penalty={newvar.penalty}, fast.beta={fast.beta}, pmethod={pmethod}"
createScripts("Classification", packagePath, "mlr_c_template", "earth", None, earth, {"degree": [1, 2, 3], "newvar.penalty": [0, 0.01, 0.2], "fast.beta": [1, 0], "pmethod": ["'backward'", "'none'"]}, summaryDict)

# polydot was super slow, so removed it
gausspr = "'classif.gausspr', kernel='{kernel}', tol={tol}"
createScripts("Classification", packagePath, "mlr_c_template", "gausspr", None, gausspr, {"kernel": ['rbfdot', 'anovadot', 'laplacedot'], "tol": ["0.0005"]}, summaryDict)

glmnet = "'classif.glmnet', alpha={alpha}"
createScripts("Classification", packagePath, "mlr_c_template", "glmnet", None, glmnet, {"alpha": [1, 0, 0.5]}, summaryDict)

h2o_deeplearning = "'classif.h2o.deeplearning', activation = '{activation}', hidden = {hidden}, epochs = {epochs}, balance_classes = {balance_classes}"
createScripts("Classification", packagePath, "mlr_c_template", "h2o.deeplearning", None, h2o_deeplearning, {"activation": ['Rectifier', 'RectifierWithDropout', 'Maxout', 'MaxoutWithDropout'], "hidden": ["c(200, 200)", "c(500, 500)"], "epochs": [10, 50], "balance_classes": ["FALSE", "TRUE"]}, summaryDict)

h2o_gbm = "'classif.h2o.gbm', ntrees = {ntrees}, nbins = {nbins}, learn_rate = {learn_rate}, balance_classes = {balance_classes}"
createScripts("Classification", packagePath, "mlr_c_template", "h2o.gbm", None, h2o_gbm, {"ntrees": [50, 500], "nbins": [20, 10], "learn_rate": [0.1, 0.05], "balance_classes": ["FALSE", "TRUE"]}, summaryDict)

h2o_randomForest = "'classif.h2o.randomForest', ntrees = {ntrees}, nbins = {nbins}, balance_classes = {balance_classes}"
createScripts("Classification", packagePath, "mlr_c_template", "h2o.randomForest", None, h2o_randomForest, {"ntrees": [50, 1000], "nbins": [20, 10, 5], "balance_classes": ["FALSE", "TRUE"]}, summaryDict)

ksvm = "'classif.ksvm', scaled = {scaled}, type = '{type}', kernel ='{kernel}', C = {C}, shrinking = {shrinking}"
createScripts("Classification", packagePath, "mlr_c_template", "ksvm", None, ksvm, {"scaled": ["TRUE", "FALSE"], "type": ["C-svc"], "kernel": ['rbfdot', 'polydot', 'vanilladot', 'laplacedot', 'anovadot'], "C": cOptions, "shrinking": ["TRUE"]}, summaryDict)

kknn = "'classif.kknn', k = {k}, distance = {distance}, kernel = '{kernel}', scale={scale}"
createScripts("Classification", packagePath, "mlr_c_template", "kknn", None, kknn, {"k": [7, 1, 10], "distance": [2], "kernel": ["optimal"], "scale": ["TRUE", "FALSE"]}, summaryDict)

mlp = "'classif.mlp', size = c({size}), maxit = {maxit}, initFunc = 'Randomize_Weights', initFuncParams = c(-0.3, 0.3), learnFunc = '{learnFunc}'"
createScripts("Classification", packagePath, "mlr_c_template", "mlp", None, mlp, {"size": [5, 50], "maxit": [100], "learnFunc": ["Std_Backpropagation", "BackpropChunk", "BackpropMomentum", "BackpropWeightDecay", "Rprop", "Quickprop", "SCG"]}, summaryDict)

multinom = "'classif.multinom'"
createScripts("Classification", packagePath, "mlr_c_template", "multinom", None, multinom, {}, summaryDict)

naiveBayes = "'classif.naiveBayes', laplace = {laplace}"
createScripts("Classification", packagePath, "mlr_c_template", "naiveBayes", None, naiveBayes, {"laplace": [0, 1]}, summaryDict)

#nnet = "'classif.nnet'"
#createScripts("Classification", packagePath, "mlr_c_template", "nnet", None, nnet, {}, summaryDict)

randomForest = "'classif.randomForest', ntree={ntree}, importance={importance}, nodesize={nodesize}"
createScripts("Classification", packagePath, "mlr_c_template", "randomForest", None, randomForest, {"ntree": [500, 1000], "importance": ["FALSE", "TRUE"], "nodesize": nodeSizeOptions}, summaryDict)

randomForestSRC = "'classif.randomForestSRC', ntree = {ntree}, bootstrap = '{bootstrap}', importance = '{importance}', proximity = '{proximity}', nodesize={nodesize}"
createScripts("Classification", packagePath, "mlr_c_template", "randomForestSRC", None, randomForestSRC, {"ntree": [1000, 100], "bootstrap": ["by.root", "by.node", "none"], "importance": ["none", "permute"], "proximity": ["inbag", "oob", "all"], "nodesize": nodeSizeOptions}, summaryDict)
#createScripts("Classification", packagePath, "mlr_c_template", "randomForestSRC", None, randomForestSRC, {"ntree": [1000, 100], "bootstrap": ["by.root", "by.node", "none"], "importance": ["none", "permute", "random", "anti"], "proximity": ["inbag", "oob", "all"], "nodesize": nodeSizeOptions}, summaryDict)

ranger = "'classif.ranger', num.trees = {num.trees}, importance = '{importance}', replace = {replace}"
createScripts("Classification", packagePath, "mlr_c_template", "ranger", None, ranger, {"num.trees": [500, 50], "importance": ['none', 'impurity', 'permutation'], "replace": ["TRUE", "FALSE"]}, summaryDict)

rda = "'classif.rda', trafo = {trafo}, simAnn = {simAnn}"
createScripts("Classification", packagePath, "mlr_c_template", "rda", None, rda, {"trafo": ["TRUE", "FALSE"], "simAnn": ["FALSE", "TRUE"]}, summaryDict)

rpart = "'classif.rpart'"
createScripts("Classification", packagePath, "mlr_c_template", "rpart", None, rpart, {}, summaryDict)

# I didn't specify proximity because I was unsure of the default value
RRF = "'classif.RRF', ntree={ntree}, replace={replace}, coefReg={coefReg}, flagReg={flagReg}"
createScripts("Classification", packagePath, "mlr_c_template", "RRF", None, RRF, {"ntree": [500, 50], "replace": ["TRUE", "FALSE"], "coefReg": [0.8, 0.9, 0.7], "flagReg": [1, 0]}, summaryDict)

# I didn't specify lambda values because I was not sure what default should be
sda = "'classif.sda', diagonal={diagonal}"
createScripts("Classification", packagePath, "mlr_c_template", "sda", None, sda, {"diagonal": ["FALSE", "TRUE"]}, summaryDict)

svm = "'classif.svm', scale = {scale}, type = '{type}', kernel = '{kernel}', cost = {cost}, shrinking = {shrinking}"
createScripts("Classification", packagePath, "mlr_c_template", "svm", None, svm, {"scale": ["TRUE", "FALSE"], "type": ["C-classification"], "kernel": ["radial", "linear", "polynomial", "sigmoid"], "cost": cOptions, "shrinking": ["TRUE"]}, summaryDict, {"kernel": "polynomial", "scale": "TRUE"})

# gblinear didn't work too well and sometimes produced NA prediction values
xgboost = "'classif.xgboost', booster='{booster}', nrounds={nrounds}, early_stopping_rounds={early_stopping_rounds}"
createScripts("Classification", packagePath, "mlr_c_template", "xgboost", None, xgboost, {"booster": ["gbtree"], "nrounds": [2, 10, 50], "early_stopping_rounds": ["NULL"]}, summaryDict)
#createScripts("Classification", packagePath, "mlr_c_template", "xgboost", None, xgboost, {"booster": ["gbtree", "gblinear"], "nrounds": [2, 10, 50], "early_stopping_rounds": ["NULL"]}, summaryDict, {"booster": "gblinear", "nrounds": 2})

## Didn't work with default params: cforest nnet gbm mda qda lda
### Also didn't work: lda, saeDNN, nnTrain, dbnDNN, mda, xyf, extraTrees, sparseLDA, gbm

#################################################################
# Feature selection
#################################################################

cforest_importance = "'cforest.importance', mincriterion='{mincriterion}', nperm={nperm}"
createScripts("FeatureSelection", packagePath, "mlr_f_template", "cforest.importance", None, cforest_importance, {"mincriterion": [0, 0.95, 0.99], "nperm": [1, 5, 10]}, summaryDict)

kruskal_test = "kruskal.test"
createScripts("FeatureSelection", packagePath, "mlr_f_template", "kruskal.test", None, kruskal_test, {}, summaryDict)

randomForestSRC_rfsrc = "'randomForestSRC.rfsrc', ntree = {ntree}, bootstrap = '{bootstrap}', nodesize={nodesize}"
createScripts("FeatureSelection", packagePath, "mlr_f_template", "randomForestSRC.rfsrc", None, randomForestSRC_rfsrc, {"ntree": [1000, 100], "bootstrap": ["by.root", "by.user", "none"], "nodesize": nodeSizeOptions}, summaryDict)
#createScripts("FeatureSelection", packagePath, "mlr_f_template", "randomForestSRC.rfsrc", None, randomForestSRC_rfsrc, {"ntree": [1000, 100], "bootstrap": ["by.root", "by.node", "none"], "importance": ["none", "permute"], "proximity": ["inbag", "oob", "all"], "nodesize": nodeSizeOptions}, summaryDict)

randomForestSRC_var_select = "'randomForestSRC.var.select', ntree = {ntree}, conservative = '{conservative}', nodesize={nodesize}"
createScripts("FeatureSelection", packagePath, "mlr_f_template", "randomForestSRC.var.select", None, randomForestSRC_var_select, {"ntree": [1000, 100], "conservative": ["medium", "low", "high"], "nodesize": nodeSizeOptions}, summaryDict)

##Failed test with default parameters = univariate.model.score, variance
## permutation.test requires a learner algorithm, but none is provided by default

if showStats:
    print("#######################################")
    for key, value in sorted(summaryDict.items()):
        print(key, value)
    print("#######################################")
    print("Total: {}".format(sum(summaryDict.values())))
    print("#######################################")
