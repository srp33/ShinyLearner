import os, sys, shutil

def createScript(algorithmType, templateFilePath, shortAlgName, algFileName, paramDict):
    scriptDir = "../{}/arff/weka/{}".format(algorithmType, shortAlgName)
    if not os.path.exists(scriptDir):
        os.makedirs(scriptDir, exist_ok=True)

    destFilePath = "{}/{}".format(scriptDir, algFileName)
    print("Saving to {}.".format(destFilePath))

    # Copy the file first to preserve permissions
    shutil.copy(templateFilePath, destFilePath)

    with open(destFilePath) as templateFile:
        template = templateFile.read()
        algorithm = replaceTokens(globals()[shortAlgName], paramDict, shortAlgName)
        template = template.replace("{algorithm}", algorithm)

    with open(destFilePath, 'w') as destFile:
        destFile.write(template)

def replaceTokens(instantiation, paramDict, shortAlgName):
    for key, value in paramDict.items():
        if "{" + key + "}" not in instantiation:
            print("A key of {} was not found in the algorithm template for {}.".format(key, shortAlgName))
            sys.exit(1)
        instantiation = instantiation.replace("{" + key + "}", str(value))

    return instantiation

#################################################################
# Classifiers
#################################################################

### The default is ZeroR. Don't use DecisionStump though because not super accurate.
###createScript("Classification, "weka_c_template", AdaBoostM1 "weka.classifiers.meta.AdaBoostM1 -P 100 -S 1 -I 10 -W weka.classifiers.trees.DecisionStump"
### Probably can use this one but not accurate enough with the default settings
##createScript("Classification", "weka_c_template", "IBk", "default", 'weka.classifiers.lazy.IBk -K 1 -W 0 -A "weka.core.neighboursearch.LinearNNSearch -A \"weka.core.EuclideanDistance -R first-last\""')
### The default is ZeroR. Don't use DecisionStump though because not super accurate.
###createScript("Classification", "weka_c_template", "LogitBoost_DecisionStump", "default", "weka.classifiers.meta.LogitBoost -P 100 -L -1.7976931348623157E308 -H 1.0 -Z 3.0 -O 1 -E 1 -S 1 -I 10 -W weka.classifiers.trees.DecisionStump -batch-size")
### The default is ZeroR. Don't use DecisionStump though because not super accurate.
###createScript("Classification", "weka_c_template", "LWL", "default", 'weka.classifiers.lazy.LWL -U 0 -K -1 -A "weka.core.neighboursearch.LinearNNSearch -A \"weka.core.EuclideanDistance -R first-last\"" -W weka.classifiers.trees.DecisionStump')

Bagging  = "weka.classifiers.meta.Bagging {representCopiesUsingWeights} -P {bagSizePercent} -S 1 -num-slots 1 -I {numIterations} -W {classifier}"
createScript("Classification", "weka_c_template", "Bagging", "default", {"representCopiesUsingWeights": "", "bagSizePercent": 100, "numIterations": 10, "classifier": "weka.classifiers.trees.REPTree -- -M 2 -V 0.001 -N 3 -S 1 -L -1 -I 0.0"})

BayesNet = "weka.classifiers.bayes.BayesNet -D -Q {searchAlgorithm} -E {estimator}"
createScript("Classification", "weka_c_template", "BayesNet", "default", {"estimator": "weka.classifiers.bayes.net.estimate.SimpleEstimator -- -A 0.5", "searchAlgorithm": "weka.classifiers.bayes.net.search.local.K2 -- -P 1 -S BAYES"})

DecisionTable = 'weka.classifiers.rules.DecisionTable {evaluationMeasure} -X 5 -S "{search}"'
createScript("Classification", "weka_c_template", "DecisionTable", "default", {"evaluationMeasure": "", "search": "weka.attributeSelection.BestFirst -D 1 -N 5"})

HoeffdingTree = "weka.classifiers.trees.HoeffdingTree -L {leafPredictionStrategy} -S {splitCriterion} -E {splitConfidence} -H {hoeffdingTieThreshold} -M {minimumFractionOfWeightInfoGain} -G {gracePeriod} -N {naiveBayesPredictionThreshold}"
createScript("Classification", "weka_c_template", "HoeffdingTree", "default", {"gracePeriod": "200.0", "hoeffdingTieThreshold": "0.05", "minimumFractionOfWeightInfoGain": "0.01", "splitConfidence": "1.0E-7", "splitCriterion": "1", "naiveBayesPredictionThreshold": "0.0", "leafPredictionStrategy": "2"})

HyperPipes = "weka.classifiers.misc.HyperPipes"
createScript("Classification", "weka_c_template", "HyperPipes", "default", {})

# Other option for pruning is -U
J48 = "weka.classifiers.trees.J48 {pruning} {subtreeRaising} {binarySplits} -M {minNumObj} {useMDLcorrection} {collapseTree} {useLaplace}"
createScript("Classification", "weka_c_template", "J48", "default", {"pruning": "-C 0.25", "useLaplace": "", "subtreeRaising": "", "binarySplits": "", "minNumObj": "2", "useMDLcorrection": "", "collapseTree": ""})

JRip = "weka.classifiers.rules.JRip -F 3 -N {minNo} -O {optimizations} -S 1 -num-decimal-places 7 {checkErrorRate} {usePruning}"
createScript("Classification", "weka_c_template", "JRip", "default", {"minNo": "2.0", "optimizations": "2", "checkErrorRate": "", "usePruning": ""})

LibLINEAR = "weka.classifiers.functions.LibLINEAR -S {SVMType} -C {cost} -E {eps} -B {bias} -L {epsilonParameter} -I {maximumNumberOfIterations} {normalize}"
createScript("Classification", "weka_c_template", "LibLINEAR", "default", {"bias": "1.0", "eps": "0.001", "cost": "1.0", "SVMType": "1", "maximumNumberOfIterations": "1000", "normalize": "", "epsilonParameter": "0.1"})

MultilayerPerceptron = "weka.classifiers.functions.MultilayerPerceptron -L {learningRate} -M {momentum} -N {trainingTime} -V {validationSetSize} -S 0 -E {validationThreshold} -H {hiddenLayers} -I {normalizeAttributes} {decay} {reset}"
createScript("Classification", "weka_c_template", "MultilayerPerceptron", "default", {"momentum": "0.2", "hiddenLayers": "a", "validationThreshold": "20", "normalizeAttributes": "", "decay": "", "validationSetSize": "0", "trainingTime": "500", "learningRate": "0.3", "reset": ""})

NaiveBayes = "weka.classifiers.bayes.NaiveBayes {useKernelEstimator} {useSupervisedDiscretization}"
createScript("Classification", "weka_c_template", "NaiveBayes", "default", {"useKernelEstimator": "", "useSupervisedDiscretization": ""})

OneR = "weka.classifiers.rules.OneR -B {minBucketSize}"
createScript("Classification", "weka_c_template", "OneR", "default", {"minBucketSize": "6"})

RandomForest = "weka.classifiers.trees.RandomForest -P {bagSizePercent} -I {numIterations} -num-slots 1 -K {numFeatures} -M 1.0 -V 0.001 -S 1 {breakTiesRandomly} {maxDepth} {calcOutOfBag}"
createScript("Classification", "weka_c_template", "RandomForest", "default", {"bagSizePercent": "100", "numIterations": "100", "breakTiesRandomly": "", "maxDepth": "", "calcOutOfBag": "", "numFeatures": "0"})

RandomTree = "weka.classifiers.trees.RandomTree -K {KValue} -M {minNum} -V {minVarianceProp} -S 1 {numFolds} {breakTiesRandomly} {maxDepth}"
createScript("Classification", "weka_c_template", "RandomTree", "default", {"minNum": "1.0", "numFolds": "", "breakTiesRandomly": "", "maxDepth": "", "minVarianceProp": "0.001", "KValue": "0"})

RBFNetwork = "weka.classifiers.functions.RBFNetwork -B {numClusters} -S 1 -R {ridge} -M {maxIts} -W {minStdDev}"
createScript("Classification", "weka_c_template", "RBFNetwork", "default", {"ridge": "1.0E-8", "maxIts": "-1", "numClusters": "2", "minStdDev": "0.1"})

REPTree = "weka.classifiers.trees.REPTree -M {minNum} -V {minVarianceProp} -N {numFolds} -S 1 -L {maxDepth} -I {initialCount} {noPruning} {spreadInitialCount}"
createScript("Classification", "weka_c_template", "REPTree", "default", {"minNum": "2", "numFolds": "3", "noPruning": "", "spreadInitialCount": "", "maxDepth": "-1", "minVarianceProp": "0.001", "initialCount": "0.0"})

SimpleLogistic = "weka.classifiers.functions.SimpleLogistic -I 0 -M 500 -H 50 -W {weightTrimBeta} {useAIC}"
createScript("Classification", "weka_c_template", "SimpleLogistic", "default", {"useAIC": "", "weightTrimBeta": "0.0"})

SMO = 'weka.classifiers.functions.SMO -C {c} -L 0.001 -P 1.0E-12 -N {filterType} -V {numFolds} -W 1 -K "{kernel}" {buildCalibrationModels} -calibrator "{calibrator}"'
createScript("Classification", "weka_c_template", "SMO", "default", {"buildCalibrationModels": "", "numFolds": "-1", "c": "1.0", "kernel": "weka.classifiers.functions.supportVector.PolyKernel -E 1.0 -C 250007", "filterType": "0", "calibrator": "weka.classifiers.functions.Logistic -R 1.0E-8 -M -1 -num-decimal-places 4"})

LibSVM = "weka.classifiers.functions.LibSVM -S 0 -K {kernelType} -D {degree} -G {gamma} -R {coef0} -N 0.5 -M 40.0 -C {cost} -E {eps} -P {loss} -B -seed 1 {shrinking} {normalize}"
createScript("Classification", "weka_c_template", "LibSVM", "default", {"loss": "0.1", "kernelType": "2", "degree": "3", "gamma": "0.0", "shrinking": "", "eps": "0.001", "cost": "1.0", "normalize": "", "coef0": "0.0"})

VFI = "weka.classifiers.misc.VFI -B {bias} {weightByConfidence}"
createScript("Classification", "weka_c_template", "VFI", "default", {"bias": "0.6", "weightByConfidence": ""})

ZeroR = "weka.classifiers.rules.ZeroR"
createScript("Classification", "weka_c_template", "ZeroR", "default", {})

#################################################################
# Feature selectors
#################################################################

Correlation = 'weka.attributeSelection.CorrelationAttributeEval -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"'
createScript("FeatureSelection", "weka_f_template", "Correlation", "default", {})

GainRatio = 'weka.attributeSelection.GainRatioAttributeEval -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"'
createScript("FeatureSelection", "weka_f_template", "GainRatio", "default", {})

InfoGain = 'weka.attributeSelection.InfoGainAttributeEval -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"'
createScript("FeatureSelection", "weka_f_template", "InfoGain", "default", {})

OneR = 'weka.attributeSelection.OneRAttributeEval -S 1 -F {folds} -B {minimumBucketSize} -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"'
createScript("FeatureSelection", "weka_f_template", "OneR", "default", {"folds": "10", "minimumBucketSize": "6"})

ReliefF = 'weka.attributeSelection.ReliefFAttributeEval -M -1 -D 1 -K {numNeighbors} {weightByDistance} -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"'
createScript("FeatureSelection", "weka_f_template", "ReliefF", "default", {"numNeighbors": "10", "weightByDistance": ""})

SVMRFE = 'weka.attributeSelection.SVMAttributeEval -X {attsToEliminatePerIteration} -Y {percentToEliminatePerIteration} -Z {percentThreshold} -P {epsilonParameter} -T {toleranceParameter} -C {complexityParameter} -N {filterType} -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"'
createScript("FeatureSelection", "weka_f_template", "SVMRFE", "default", {"percentThreshold": "1", "filterType": "0", "toleranceParameter": "1.0E-10", "complexityParameter": "1.0", "attsToEliminatePerIteration": "0", "epsilonParameter": "1.0E-25", "percentToEliminatePerIteration": "10"})

SymmetricalUncertainty = 'weka.attributeSelection.SymmetricalUncertAttributeEval -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"'
createScript("FeatureSelection", "weka_f_template", "SymmetricalUncertainty", "default", {})
