import os, sys
from build_scripts_helper import *

showStats = sys.argv[1] == "True"

summaryDict = {}

#################################################################
# Meta options
#################################################################

packagePath = "arff/weka"

metaClassifiers = ["weka.classifiers.trees.REPTree -- -M 2 -V 0.001 -N 3 -S 1 -L -1 -I 0.0", "weka.classifiers.trees.J48 -- -C 0.25 -M 2", 'weka.classifiers.lazy.IBk -- -K 1 -W 0 -A "weka.core.neighboursearch.LinearNNSearch -- -A \"weka.core.EuclideanDistance -R first-last\""', 'weka.classifiers.functions.SimpleLogistic -- -I 0 -M 500 -H 50 -W 0.0']
cOptions = ["1.0", "0.1", "10.0", "100.0"]

#################################################################
# Classifiers
#################################################################

Bagging  = "weka.classifiers.meta.Bagging {representCopiesUsingWeights} -P {bagSizePercent} -S 1 -num-slots 1 -I {numIterations} -W {classifier}"
createScripts("Classification", packagePath, "weka_c_template", "Bagging", None, Bagging, {"representCopiesUsingWeights": ["", "-represent-copies-using-weights"], "bagSizePercent": [75, 100], "numIterations": [10, 100], "classifier": metaClassifiers}, summaryDict)

# Some of these search algorithms are extremely slow or don't work at all, so I removed them.
BayesNet = "weka.classifiers.bayes.BayesNet -D -Q {searchAlgorithm} -E {estimator}"
#createScripts("Classification", packagePath, "weka_c_template", "BayesNet", None, BayesNet, {"estimator": ["weka.classifiers.bayes.net.estimate.SimpleEstimator -- -A 0.5", "weka.classifiers.bayes.net.estimate.BayesNetEstimator -- -A 0.5", "weka.classifiers.bayes.net.estimate.BMAEstimator -- -A 0.5", "weka.classifiers.bayes.net.estimate.MultiNomialBMAEstimator -- -k2"], "searchAlgorithm": ["weka.classifiers.bayes.net.search.local.K2 -- -P 1 -S BAYES", "weka.classifiers.bayes.net.search.local.EBMC -- -T 2 -P 2 -C 2 -S K2", "weka.classifiers.bayes.net.search.local.GeneticSearch -- -L 10 -A 100 -U 10 -R 1 -M -C -S BAYES", "weka.classifiers.bayes.net.search.local.HillClimber -- -P 1 -S BAYES", "weka.classifiers.bayes.net.search.local.LAGDHillClimber -- -L 2 -G 5 -P 1 -S BAYES", "weka.classifiers.bayes.net.search.local.RepeatedHillClimber -- -U 10 -A 1 -P 1 -S BAYES", "weka.classifiers.bayes.net.search.local.SimulatedAnnealing -- -A 10.0 -U 10000 -D 0.999 -R 1 -S BAYES", "weka.classifiers.bayes.net.search.local.TabuSearch -- -L 5 -U 10 -P 1 -S BAYES", "weka.classifiers.bayes.net.search.local.TAN -- -S BAYES"]}, summaryDict)
#createScripts("Classification", packagePath, "weka_c_template", "BayesNet", None, BayesNet, {"estimator": ["weka.classifiers.bayes.net.estimate.SimpleEstimator -- -A 0.5", "weka.classifiers.bayes.net.estimate.BMAEstimator -- -A 0.5"], "searchAlgorithm": ["weka.classifiers.bayes.net.search.local.K2 -- -P 1 -S BAYES", "weka.classifiers.bayes.net.search.local.HillClimber -- -P 1 -S BAYES"]}, summaryDict)
createScripts("Classification", packagePath, "weka_c_template", "BayesNet", None, BayesNet, {"estimator": ["weka.classifiers.bayes.net.estimate.SimpleEstimator -- -A 0.5", "weka.classifiers.bayes.net.estimate.BMAEstimator -- -A 0.5"], "searchAlgorithm": ["weka.classifiers.bayes.net.search.local.K2 -- -P 1 -S BAYES"]}, summaryDict)

DecisionTable = 'weka.classifiers.rules.DecisionTable {evaluationMeasure} -X 5 -S "{search}"'
createScripts("Classification", packagePath, "weka_c_template", "DecisionTable", None, DecisionTable, {"evaluationMeasure": ["", "-E auc", "-E rmse"], "search": ["weka.attributeSelection.BestFirst -D 1 -N 5", "weka.attributeSelection.GreedyStepwise -T -1.7976931348623157E308 -N -1 -num-slots 1"]}, summaryDict)

HoeffdingTree = "weka.classifiers.trees.HoeffdingTree -L {leafPredictionStrategy} -S {splitCriterion} -E {splitConfidence} -H {hoeffdingTieThreshold} -M {minimumFractionOfWeightInfoGain} -G {gracePeriod} -N {naiveBayesPredictionThreshold}"
createScripts("Classification", packagePath, "weka_c_template", "HoeffdingTree", None, HoeffdingTree, {"gracePeriod": ["100.0", "300.0"], "hoeffdingTieThreshold": ["0.02", "0.10"], "minimumFractionOfWeightInfoGain": ["0.01"], "splitConfidence": ["1.0E-7", "1.0E-5"], "splitCriterion": ["1", "0"], "naiveBayesPredictionThreshold": ["0.0"], "leafPredictionStrategy": ["2", "1"]}, summaryDict)

HyperPipes = "weka.classifiers.misc.HyperPipes"
createScripts("Classification", packagePath, "weka_c_template", "HyperPipes", None, HyperPipes, {}, summaryDict)

# Other option for pruning is -U
J48 = "weka.classifiers.trees.J48 {pruning} {subtreeRaising} {binarySplits} -M {minNumObj} {useMDLcorrection} {collapseTree} {useLaplace}"
createScripts("Classification", packagePath, "weka_c_template", "J48", None, J48, {"pruning": ["-C 0.25", "-U"], "useLaplace": ["", "-A"], "subtreeRaising": ["", "-S"], "binarySplits": ["", "-B"], "minNumObj": ["2", "5"], "useMDLcorrection": ["", "-J"], "collapseTree": ["", "-O"]}, summaryDict, {"pruning": "-U", "subtreeRaising": "-S"})

# The usePruning -P option throws errors, so I removed it
JRip = "weka.classifiers.rules.JRip -F 3 -N {minNo} -O {optimizations} -S 1 -num-decimal-places 7 {checkErrorRate} {usePruning}"
createScripts("Classification", packagePath, "weka_c_template", "JRip", None, JRip, {"minNo": ["2.0", "4.0", "6.0"], "optimizations": ["2", "5"], "checkErrorRate": ["", "-E"], "usePruning": [""]}, summaryDict)

LibLINEAR = "weka.classifiers.functions.LibLINEAR -S {SVMType} -C {cost} -E {eps} -B {bias} -P -L {epsilonParameter} -I {maximumNumberOfIterations} {normalize}"
createScripts("Classification", packagePath, "weka_c_template", "LibLINEAR", None, LibLINEAR, {"bias": ["1.0", "-1.0"], "eps": ["0.001"], "cost": cOptions, "SVMType": ["0"], "maximumNumberOfIterations": ["1000"], "normalize": ["", "-Z"], "epsilonParameter": ["0.1"]}, summaryDict)

LibSVM = "weka.classifiers.functions.LibSVM -S 0 -K {kernelType} -D {degree} -G {gamma} -R {coef0} -N 0.5 -M 40.0 -C {cost} -E {eps} -P {loss} -B -seed 1 {shrinking} {normalize}"
createScripts("Classification", packagePath, "weka_c_template", "LibSVM", None, LibSVM, {"loss": ["0.1"], "kernelType": ["2", "0", "1", "3"], "degree": ["3"], "gamma": ["0.0"], "shrinking": [""], "eps": ["0.001"], "cost": cOptions, "normalize": ["", "-Z"], "coef0": ["0.0"]}, summaryDict)

MultilayerPerceptron = "weka.classifiers.functions.MultilayerPerceptron -L {learningRate} -M {momentum} -N {trainingTime} -V {validationSetSize} -S 0 -E {validationThreshold} -H {hiddenLayers} {normalizeAttributes} {decay} {reset}"
createScripts("Classification", packagePath, "weka_c_template", "MultilayerPerceptron", None, MultilayerPerceptron, {"momentum": ["0.2", "0.1", "0.3"], "hiddenLayers": ["a", "i", "o", "t"], "validationThreshold": ["20"], "normalizeAttributes": ["", "-I"], "decay": ["", "-D"], "validationSetSize": ["0"], "trainingTime": ["500"], "learningRate": ["0.3"], "reset": ["", "-R"]}, summaryDict)

NaiveBayes = "weka.classifiers.bayes.NaiveBayes {useKernelEstimator} {useSupervisedDiscretization}"
createScripts("Classification", packagePath, "weka_c_template", "NaiveBayes", None, NaiveBayes, {"useKernelEstimator": ["", "-K"], "useSupervisedDiscretization": ["", "-D"]}, summaryDict, {"useKernelEstimator": "-K", "useSupervisedDiscretization": "-D"})

OneR = "weka.classifiers.rules.OneR -B {minBucketSize}"
createScripts("Classification", packagePath, "weka_c_template", "OneR", None, OneR, {"minBucketSize": ["6", "3", "9"]}, summaryDict)

RandomForest = "weka.classifiers.trees.RandomForest -P {bagSizePercent} -I {numIterations} -num-slots 1 -K {numFeatures} -M 1.0 -V 0.001 -S 1 {breakTiesRandomly} {maxDepth} {calcOutOfBag}"
createScripts("Classification", packagePath, "weka_c_template", "RandomForest", None, RandomForest, {"bagSizePercent": ["100"], "numIterations": ["100", "50", "1000"], "breakTiesRandomly": ["", "-B"], "maxDepth": [""], "calcOutOfBag": [""], "numFeatures": ["0", "5", "10"]}, summaryDict)

RandomTree = "weka.classifiers.trees.RandomTree -K {KValue} -M {minNum} -V {minVarianceProp} -S 1 {numFolds} {breakTiesRandomly} {maxDepth}"
createScripts("Classification", packagePath, "weka_c_template", "RandomTree", None, RandomTree, {"minNum": ["1.0"], "numFolds": [""], "breakTiesRandomly": ["", "-B"], "maxDepth": [""], "minVarianceProp": ["0.001"], "KValue": ["0"]}, summaryDict)

RBFNetwork = "weka.classifiers.functions.RBFNetwork -B {numClusters} -S 1 -R {ridge} -M {maxIts} -W {minStdDev}"
createScripts("Classification", packagePath, "weka_c_template", "RBFNetwork", None, RBFNetwork, {"ridge": ["1.0E-8", "1.0E-6"], "maxIts": ["-1"], "numClusters": ["2", "4", "6"], "minStdDev": ["0.1", "0.05", "0.2"]}, summaryDict)

REPTree = "weka.classifiers.trees.REPTree -M {minNum} -V {minVarianceProp} -N {numFolds} -S 1 -L {maxDepth} -I {initialCount} {noPruning} {spreadInitialCount}"
createScripts("Classification", packagePath, "weka_c_template", "REPTree", None, REPTree, {"minNum": ["2", "5"], "numFolds": ["3"], "noPruning": ["", "-P"], "spreadInitialCount": ["", "-R"], "maxDepth": ["-1"], "minVarianceProp": ["0.001", "0.01"], "initialCount": ["0.0"]}, summaryDict)

SimpleLogistic = "weka.classifiers.functions.SimpleLogistic -I 0 -M 500 -H 50 -W {weightTrimBeta} {useAIC}"
createScripts("Classification", packagePath, "weka_c_template", "SimpleLogistic", None, SimpleLogistic, {"useAIC": ["", "-A"], "weightTrimBeta": ["0.0", "0.1", "0.5"]}, summaryDict, {"useAIC": "","weightTrimBeta": "0.5"})

SMO = 'weka.classifiers.functions.SMO -C {c} -L 0.001 -P 1.0E-12 -N {filterType} -V {numFolds} -W 1 -K "{kernel}" {buildCalibrationModels} -calibrator "{calibrator}"'
createScripts("Classification", packagePath, "weka_c_template", "SMO", None, SMO, {"buildCalibrationModels": [""], "numFolds": ["-1"], "c": cOptions, "kernel": ["weka.classifiers.functions.supportVector.PolyKernel -E 1.0 -C 250007", "weka.classifiers.functions.supportVector.RBFKernel -G 0.01 -C 250007"], "filterType": ["0", "1", "2"], "calibrator": ["weka.classifiers.functions.Logistic -R 1.0E-8 -M -1 -num-decimal-places 4"]}, summaryDict, {"c": 0.1, "kernel": "weka.classifiers.functions.supportVector.RBFKernel -G 0.01 -C 250007"}, {"c": 1.0, "filterType": "1", "kernel": "weka.classifiers.functions.supportVector.RBFKernel -G 0.01 -C 250007"})

VFI = "weka.classifiers.misc.VFI -B {bias} {weightByConfidence}"
createScripts("Classification", packagePath, "weka_c_template", "VFI", None, VFI, {"bias": ["0.6", "0.3", "0.9"], "weightByConfidence": ["", "-C"]}, summaryDict)

ZeroR = "weka.classifiers.rules.ZeroR"
createScripts("Classification", packagePath, "weka_c_template", "ZeroR", None, ZeroR, {}, summaryDict)

### The default is ZeroR. Don't use DecisionStump though because not super accurate.
###createScripts("Classification, "weka_c_template", AdaBoostM1 "weka.classifiers.meta.AdaBoostM1 -P 100 -S 1 -I 10 -W weka.classifiers.trees.DecisionStump"
### Probably can use this one but not accurate enough with the default settings
##createScripts("Classification", packagePath, "weka_c_template", "IBk", None, 'weka.classifiers.lazy.IBk -K 1 -W 0 -A "weka.core.neighboursearch.LinearNNSearch -A \"weka.core.EuclideanDistance -R first-last\""')
### The default is ZeroR. Don't use DecisionStump though because not super accurate.
###createScripts("Classification", packagePath, "weka_c_template", "LogitBoost_DecisionStump", None, "weka.classifiers.meta.LogitBoost -P 100 -L -1.7976931348623157E308 -H 1.0 -Z 3.0 -O 1 -E 1 -S 1 -I 10 -W weka.classifiers.trees.DecisionStump -batch-size")
### The default is ZeroR. Don't use DecisionStump though because not super accurate.
###createScripts("Classification", packagePath, "weka_c_template", "LWL", None, 'weka.classifiers.lazy.LWL -U 0 -K -1 -A "weka.core.neighboursearch.LinearNNSearch -A \"weka.core.EuclideanDistance -R first-last\"" -W weka.classifiers.trees.DecisionStump')

#################################################################
# Feature selectors
#################################################################

# There are no hyperparameters for this algorithm.
Correlation = 'weka.attributeSelection.CorrelationAttributeEval -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"'
createScripts("FeatureSelection", packagePath, "weka_f_template", "Correlation", None, Correlation, {}, summaryDict)

# There are no hyperparameters for this algorithm.
GainRatio = 'weka.attributeSelection.GainRatioAttributeEval -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"'
createScripts("FeatureSelection", packagePath, "weka_f_template", "GainRatio", None, GainRatio, {}, summaryDict)

InfoGain = 'weka.attributeSelection.InfoGainAttributeEval {binarize} -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"'
createScripts("FeatureSelection", packagePath, "weka_f_template", "InfoGain", None, InfoGain, {"binarize": ["", "-B"]}, summaryDict)

OneR = 'weka.attributeSelection.OneRAttributeEval -S 1 -F {folds} -B {minimumBucketSize} -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"'
createScripts("FeatureSelection", packagePath, "weka_f_template", "OneR", None, OneR, {"folds": ["10"], "minimumBucketSize": ["6", "3", "10"]}, summaryDict)

ReliefF = 'weka.attributeSelection.ReliefFAttributeEval -M -1 -D 1 -K {numNeighbors} {weightByDistance} -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"'
createScripts("FeatureSelection", packagePath, "weka_f_template", "ReliefF", None, ReliefF, {"numNeighbors": ["10", "5", "1"], "weightByDistance": ["", "-W"]}, summaryDict)

SVMRFE = 'weka.attributeSelection.SVMAttributeEval -X {attsToEliminatePerIteration} -Y {percentToEliminatePerIteration} -Z {percentThreshold} -P {epsilonParameter} -T {toleranceParameter} -C {complexityParameter} -N {filterType} -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"'
createScripts("FeatureSelection", packagePath, "weka_f_template", "SVMRFE", None, SVMRFE, {"percentThreshold": ["1", "5", "10"], "filterType": ["0"], "toleranceParameter": ["1.0E-10", "1.0e-8", "1.0e-6"], "complexityParameter": cOptions, "attsToEliminatePerIteration": ["0"], "epsilonParameter": ["1.0E-25"], "percentToEliminatePerIteration": ["10"]}, summaryDict)

# There are no hyperparameters for this algorithm.
SymmetricalUncertainty = 'weka.attributeSelection.SymmetricalUncertAttributeEval -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"'
createScripts("FeatureSelection", packagePath, "weka_f_template", "SymmetricalUncertainty", None, SymmetricalUncertainty, {}, summaryDict)

#OneR_Wrapper = 'weka.attributeSelection.WrapperSubsetEval -B weka.classifiers.rules.OneR -F 5 -T 0.01 -R 1 -E AUC -- -B 6 -s \"weka.attributeSelection.GreedyStepwise -R -T -1.7976931348623157E308 -N -1 -num-slots 1\"'
#createScripts("FeatureSelection", packagePath, "weka_f_template", "OneR_Wrapper", None, OneR_Wrapper, {}, summaryDict)

#SMO_Wrapper = 'weka.attributeSelection.WrapperSubsetEval -B weka.classifiers.functions.SMO -F 5 -T 0.01 -R 1 -E AUC -- -C 1.0 -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 -K \"weka.classifiers.functions.supportVector.PolyKernel -E 1.0 -C 250007\" -calibrator \"weka.classifiers.functions.Logistic -R 1.0E-8 -M -1 -num-decimal-places 4\" -s \"weka.attributeSelection.GreedyStepwise -R -T -1.7976931348623157E308 -N -1 -num-slots 1\"'
#createScripts("FeatureSelection", packagePath, "weka_f_template", "SMO_Wrapper", None, SMO_Wrapper, {}, summaryDict)

#RandomForest_Wrapper = 'weka.attributeSelection.WrapperSubsetEval -B weka.classifiers.trees.RandomForest -F 5 -T 0.01 -R 1 -E AUC -- -P 100 -I 100 -num-slots 1 -K 0 -M 1.0 -V 0.001 -S 1 -s \"weka.attributeSelection.GreedyStepwise -R -T -1.7976931348623157E308 -N -1 -num-slots 1\"'
#createScripts("FeatureSelection", packagePath, "weka_f_template", "RandomForest_Wrapper", None, RandomForest_Wrapper, {}, summaryDict)

if showStats:
    print("#######################################")
    for key, value in sorted(summaryDict.items()):
        print(key, value)
    print("#######################################")
    print("Total: {}".format(sum(summaryDict.values())))
    print("#######################################")
