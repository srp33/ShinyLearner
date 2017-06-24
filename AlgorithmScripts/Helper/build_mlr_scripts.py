import os, sys, shutil

def createScript(algorithmType, templateFilePath, shortAlgName, algFileName, algName):
    scriptDir = "../{}/tsv/mlr/{}".format(algorithmType, shortAlgName)
    if not os.path.exists(scriptDir):
        os.makedirs(scriptDir, exist_ok=True)

    destFilePath = "{}/{}".format(scriptDir, algFileName)
    print("Saving to {}.".format(destFilePath))

    # Copy the file first to preserve permissions
    shutil.copy(templateFilePath, destFilePath)

    with open(destFilePath) as templateFile:
        template = templateFile.read()
        template = template.replace("{algorithm}", algName)

    with open(destFilePath, 'w') as destFile:
        destFile.write(template)

## Focused on algorithms that support probabilistic predictions, multiclass and numerical + factor values. Some have been excluded because they don't work.

createScript("Classification", "mlr_c_template", "boosting", "default", "boosting")
createScript("Classification", "mlr_c_template", "C50", "default", "C50")
createScript("Classification", "mlr_c_template", "ctree", "default", "ctree")
createScript("Classification", "mlr_c_template", "cvglmnet", "default", "cvglmnet")
createScript("Classification", "mlr_c_template", "gausspr", "default", "gausspr")
createScript("Classification", "mlr_c_template", "glmnet", "default", "glmnet")
createScript("Classification", "mlr_c_template", "h2o.gbm", "default", "h2o.gbm")
createScript("Classification", "mlr_c_template", "h2o.deeplearning", "default", "h2o.deeplearning")
createScript("Classification", "mlr_c_template", "h2o.randomForest", "default", "h2o.randomForest")
createScript("Classification", "mlr_c_template", "kknn", "default", "ksvm")
createScript("Classification", "mlr_c_template", "mlp", "default", "mlp")
createScript("Classification", "mlr_c_template", "multinom", "default", "multinom")
createScript("Classification", "mlr_c_template", "naiveBayes", "default", "naiveBayes")
createScript("Classification", "mlr_c_template", "randomForest", "default", "randomForest")
createScript("Classification", "mlr_c_template", "randomForestSRC", "default", "randomForestSRC")
createScript("Classification", "mlr_c_template", "ranger", "default", "ranger")
createScript("Classification", "mlr_c_template", "rda", "default", "rda")
createScript("Classification", "mlr_c_template", "rpart", "default", "rpart")
createScript("Classification", "mlr_c_template", "sda", "default", "sda")
createScript("Classification", "mlr_c_template", "svm", "default", "svm")
createScript("Classification", "mlr_c_template", "xgboost", "default", "xgboost")

## Didn't work with default params: cforest nnet gbm mda qda lda
### Also didn't work: lda, saeDNN, nnTrain, dbnDNN, mda, xyf, extraTrees, sparseLDA, gbm

createScript("FeatureSelection", "mlr_f_template", "cforest.importance", "default", "cforest.importance")
createScript("FeatureSelection", "mlr_f_template", "kruskal.test", "default", "kruskal.test")
createScript("FeatureSelection", "mlr_f_template", "randomForestSRC.rfsrc", "default", "randomForestSRC.rfsrc")
createScript("FeatureSelection", "mlr_f_template", "randomForestSRC.var.select", "default", "randomForestSRC.var.select")

#####################################################################
#####################################################################
#####################################################################
##Failed test with default parameters = univariate.model.score, variance
## permutation.test requires a learner algorithm, but none is provided by default

###python MakeParameterCombinationFiles.py $baseDir/mlr__rf.min.depth method=md,vh,vh.vimp conservative=medium,low,high nodesize=2,3,4 nrep=50,100 nstep=1,5
#
#### mlr naive bayes
###laplace
###1
###10
###100
###1000
###10000
