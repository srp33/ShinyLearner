import os, sys
from build_scripts_helper import *

#################################################################
# Meta options
#################################################################

packagePath = "tsv/mlr"

cOptions = [1.0, 0.01, 0.1, 10.0]

#################################################################
# Classification
#################################################################

## Focused on algorithms that support probabilistic predictions, multiclass and numerical + factor values. Some have been excluded because they don't work.

#createScripts("Classification", packagePath, "weka_c_template", "Bagging", None, Bagging, {"representCopiesUsingWeights": [""], "bagSizePercent": [100], "numIterations": [10], "classifier": ["weka.classifiers.trees.REPTree -- -M 2 -V 0.001 -N 3 -S 1 -L -1 -I 0.0"]})

boosting = "'classif.boosting', boos={boos}, mfinal={mfinal}, coeflearn='{coeflearn}'"
createScripts("Classification", packagePath, "mlr_c_template", "boosting", None, boosting, {"boos": ["TRUE", "FALSE"], "mfinal": [100, 50, 1000], "coeflearn": ["Breiman", "Freund"]})

C50 = "'classif.C50', subset = {subset}, winnow = {winnow}, noGlobalPruning = {noGlobalPruning}, CF = {CF}, minCases = {minCases}, fuzzyThreshold = {fuzzyThreshold}, sample = {sample}, earlyStopping = {earlyStopping}"
createScripts("Classification", packagePath, "mlr_c_template", "C50", None, C50, {"subset": ["FALSE", "TRUE"], "winnow": ["FALSE", "TRUE"], "noGlobalPruning": ["FALSE", "TRUE"], "CF": [0.25], "minCases": [2], "fuzzyThreshold": ["FALSE", "TRUE"], "sample": [0], "earlyStopping": ["TRUE", "FALSE"]})

ctree = "'classif.ctree', teststat = '{teststat}', testtype = '{testtype}', mincriterion = {mincriterion}, minsplit = {minsplit}, minbucket = {minbucket}, stump = {stump}, nresample = {nresample}"
createScripts("Classification", packagePath, "mlr_c_template", "ctree", None, ctree, {"teststat": ['quad', 'max'], "testtype": ['Bonferroni', 'MonteCarlo', 'Univariate', 'Teststatistic'], "mincriterion": [0.95], "minsplit": [20], "minbucket": [7], "stump": ["FALSE", "TRUE"], "nresample": [9999]})

gausspr = "'classif.gausspr', kernel='{kernel}', tol={tol}"
createScripts("Classification", packagePath, "mlr_c_template", "gausspr", None, gausspr, {"kernel": ['rbfdot', 'polydot', 'vanilladot', 'tanhdot', 'laplacedot', 'besseldot', 'anovadot', 'splinedot', 'stringdot'], "tol": ["0.0005"]})

glmnet = "'classif.glmnet', alpha={alpha}"
createScripts("Classification", packagePath, "mlr_c_template", "glmnet", None, glmnet, {"alpha": [1, 0, 0.5]})

h2o_deeplearning = "'classif.h2o.deeplearning', activation = '{activation}', hidden = {hidden}, epochs = {epochs}, balance_classes = {balance_classes}, autoencoder = {autoencoder}"
createScripts("Classification", packagePath, "mlr_c_template", "h2o.deeplearning", None, h2o_deeplearning, {"activation": ['Tanh', 'TanhWithDropout', 'Rectifier', 'RectifierWithDropout', 'Maxout', 'MaxoutWithDropout'], "hidden": ["c(200, 200)", "c(100, 100)", "c(500, 500)"], "epochs": [10, 20, 50], "balance_classes": ["FALSE", "TRUE"], "autoencoder": ["FALSE", "TRUE"]})

h2o_gbm = "'classif.h2o.gbm', ntrees = {ntrees}, nbins = {nbins}, learn_rate = {learn_rate}, balance_classes = {balance_classes}"
createScripts("Classification", packagePath, "mlr_c_template", "h2o.gbm", None, h2o_gbm, {"ntrees": [50, 100, 1000], "nbins": [20, 5, 10], "learn_rate": [0.1, 0.05, 0.3], "balance_classes": ["FALSE", "TRUE"]})

h2o_randomForest = "'classif.h2o.randomForest', ntrees = {ntrees}, nbins = {nbins}, balance_classes = {balance_classes}"
createScripts("Classification", packagePath, "mlr_c_template", "h2o.randomForest", None, h2o_randomForest, {"ntrees": [50, 100, 1000], "nbins": [20, 5, 10], "balance_classes": ["FALSE", "TRUE"]})

ksvm = "'classif.ksvm', scaled = {scaled}, type = '{type}', kernel ='{kernel}', C = {C}, shrinking = {shrinking}"
createScripts("Classification", packagePath, "mlr_c_template", "ksvm", None, ksvm, {"scaled": ["TRUE", "FALSE"], "type": ["C-svc", "nu-svc", "C-bsvc"], "kernel": ['rbfdot', 'polydot', 'vanilladot', 'tanhdot', 'laplacedot', 'besseldot', 'anovadot', 'splinedot', 'stringdot'], "C": cOptions, "shrinking": ["TRUE", "FALSE"]})

kknn = "'classif.kknn', k = {k}, distance = {distance}, kernel = '{kernel}', scale={scale}"
createScripts("Classification", packagePath, "mlr_c_template", "kknn", None, kknn, {"k": [7, 1, 10], "distance": [2], "kernel": ["optimal"], "scale": ["TRUE", "FALSE"]})

mlp = "'classif.mlp', size = c({size}), maxit = {maxit}, initFunc = 'Randomize_Weights', initFuncParams = c(-0.3, 0.3), learnFunc = '{learnFunc}'"
createScripts("Classification", packagePath, "mlr_c_template", "mlp", None, mlp, {"size": [5, 10, 50], "maxit": [100], "learnFunc": ["Std_Backpropagation", "BackpropBatch", "BackpropChunk", "BackpropMomentum", "BackpropWeightDecay", "Rprop", "Quickprop", "SCG"]})

multinom = "'classif.multinom'"
createScripts("Classification", packagePath, "mlr_c_template", "multinom", None, multinom, {})

naiveBayes = "'classif.naiveBayes', laplace = {laplace}"
createScripts("Classification", packagePath, "mlr_c_template", "naiveBayes", None, naiveBayes, {"laplace": [0, 1]})

randomForest = "'classif.randomForest', ntree={ntree}, importance={importance}"
createScripts("Classification", packagePath, "mlr_c_template", "randomForest", None, randomForest, {"ntree": [500, 50, 1000], "importance": ["FALSE", "TRUE"]})

randomForestSRC = "'classif.randomForestSRC', ntree = {ntree}, bootstrap = '{bootstrap}', importance = '{importance}', proximity = '{proximity}'"
createScripts("Classification", packagePath, "mlr_c_template", "randomForestSRC", None, randomForestSRC, {"ntree": [1000, 50, 100], "bootstrap": ["by.root", "by.node", "none"], "importance": ["none", "permute", "random", "anti", "permute.ensemble", "random.ensemble", "anti.ensemble"], "proximity": ["inbag", "oob", "all"]})

ranger = "'classif.ranger', num.trees = {num.trees}, importance = '{importance}', replace = {replace}"
createScripts("Classification", packagePath, "mlr_c_template", "ranger", None, ranger, {"num.trees": [500, 50, 1000], "importance": ['none', 'impurity', 'permutation'], "replace": ["TRUE", "FALSE"]})

rda = "'classif.rda', trafo = {trafo}, simAnn = {simAnn}"
createScripts("Classification", packagePath, "mlr_c_template", "rda", None, rda, {"trafo": ["TRUE", "FALSE"], "simAnn": ["FALSE", "TRUE"]})

rpart = "'classif.rpart'"
createScripts("Classification", packagePath, "mlr_c_template", "rpart", None, rpart, {})

# I didn't specify proximity because I was unsure of the default value
RRF = "'classif.RRF', ntree={ntree}, replace={replace}, coefReg={coefReg}, flagReg={flagReg}"
createScripts("Classification", packagePath, "mlr_c_template", "RRF", None, RRF, {"ntree": [500, 50, 1000], "replace": ["TRUE", "FALSE"], "coefReg": [0.8, 0.5, 0.9], "flagReg": [1, 0]})

# I didn't specify lambda values because I was not sure what default should be
sda = "'classif.sda', diagonal={diagonal}"
createScripts("Classification", packagePath, "mlr_c_template", "sda", None, sda, {"diagonal": ["FALSE", "TRUE"]})

svm = "'classif.svm', scale = {scale}, type = '{type}', kernel = '{kernel}', cost = {cost}, shrinking = {shrinking}"
createScripts("Classification", packagePath, "mlr_c_template", "svm", None, svm, {"scale": ["TRUE", "FALSE"], "type": ["C-classification", "nu-classification"], "kernel": ["linear", "polynomial", "radial basis", "sigmoid"], "cost": cOptions, "shrinking": ["TRUE", "FALSE"]})

xgboost = "'classif.xgboost', booster='{booster}', nrounds={nrounds}, early_stopping_rounds={early_stopping_rounds}"
createScripts("Classification", packagePath, "mlr_c_template", "xgboost", None, xgboost, {"booster": ["gbtree", "gblinear"], "nrounds": [2, 5, 10], "early_stopping_rounds": ["NULL", 5, 20]})

## Didn't work with default params: cforest nnet gbm mda qda lda
### Also didn't work: lda, saeDNN, nnTrain, dbnDNN, mda, xyf, extraTrees, sparseLDA, gbm

#################################################################
# Feature selection
#################################################################

cforest_importance = "cforest.importance"
createScripts("FeatureSelection", packagePath, "mlr_f_template", "cforest.importance", None, cforest_importance, {})

kruskal_test = "kruskal.test"
createScripts("FeatureSelection", packagePath, "mlr_f_template", "kruskal.test", None, kruskal_test, {})

randomForestSRC_rfsrc = "randomForestSRC.rfsrc"
createScripts("FeatureSelection", packagePath, "mlr_f_template", "randomForestSRC.rfsrc", None, randomForestSRC_rfsrc, {})

randomForestSRC_var_select = "randomForestSRC.var.select"
createScripts("FeatureSelection", packagePath, "mlr_f_template", "randomForestSRC.var.select", None, randomForestSRC_var_select, {})

##Failed test with default parameters = univariate.model.score, variance
## permutation.test requires a learner algorithm, but none is provided by default
