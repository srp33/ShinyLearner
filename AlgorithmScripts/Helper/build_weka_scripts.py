import os, sys
from build_scripts_helper import *

#################################################################
# Meta options
#################################################################

packagePath = "arff/weka"

metaClassifiers = ["weka.classifiers.trees.REPTree -- -M 2 -V 0.001 -N 3 -S 1 -L -1 -I 0.0", "weka.classifiers.trees.J48 -- -C 0.25 -M 2", 'weka.classifiers.lazy.IBk -K 1 -W 0 -A "weka.core.neighboursearch.LinearNNSearch -A \"weka.core.EuclideanDistance -R first-last\""', 'weka.classifiers.functions.LibLINEAR -S 1 -C 1.0 -E 0.001 -B 1.0 -L 0.1 -I 1000', 'weka.classifiers.functions.SimpleLogistic -I 0 -M 500 -H 50 -W 0.0', 'weka.classifiers.functions.MultilayerPerceptron -L 0.3 -M 0.2 -N 500 -V 0 -S 0 -E 20 -H a', 'weka.classifiers.functions.SGD -F 0 -L 0.01 -R 1.0E-4 -E 500 -C 0.001 -S 1', 'weka.classifiers.functions.LibSVM -S 0 -K 2 -D 3 -G 0.0 -R 0.0 -N 0.5 -M 40.0 -C 1.0 -E 0.001 -P 0.1 -seed 1']
searchAlgorithms = ["weka.attributeSelection.BestFirst -D 1 -N 5", "weka.attributeSelection.EvolutionarySearch -population-size 20 -generations 20 -init-op 0 -selection-op 1 -crossover-op 0 -crossover-probability 0.6 -mutation-op 0 -mutation-probability 0.01 -replacement-op 0 -seed 1 -report-frequency 20", "weka.attributeSelection.GreedyStepwise -T -1.7976931348623157E308 -N -1 -num-slots 1", 'weka.attributeSelection.KMedoidsSampling -P 2 -Q 2 -N 2 -V weka.attributeSelection.ssf.validationCriteria.SimplifiedSilhouette -D "weka.attributeSelection.ssf.distanceFunctions.SymmetricalUncertainty -F \"weka.filters.unsupervised.attribute.PKIDiscretize -R first-last\""', 'weka.attributeSelection.IWSS -minFolds 2 -theta 1.0 -rankingMetric "weka.attributeSelection.SymmetricalUncertAttributeEval "', "weka.attributeSelection.IWSSembeddedNB -minFolds 2 -theta 1.0", "weka.attributeSelection.ScatterSearchV1 -T 0.0 -Z -1 -R 0 -S 1 -D", "weka.attributeSelection.PSOSearch -N 20 -I 20 -T 0 -M 0.01 -A 0.33 -B 0.33 -C 0.34 -R 20 -S 1", "weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1", "weka.attributeSelection.TabuSearch -Z -1 -P 1.0 -S 1 -N -1"]
cOptions = [1.0, 0.01, 0.1, 10.0]

#################################################################
# Classifiers
#################################################################

Bagging  = "weka.classifiers.meta.Bagging {representCopiesUsingWeights} -P {bagSizePercent} -S 1 -num-slots 1 -I {numIterations} -W {classifier}"
createScripts("Classification", packagePath, "weka_c_template", "Bagging", None, Bagging, {"representCopiesUsingWeights": ["", "-represent-copies-using-weights"], "bagSizePercent": [75, 100], "numIterations": [10, 50, 100], "classifier": metaClassifiers})

BayesNet = "weka.classifiers.bayes.BayesNet -D -Q {searchAlgorithm} -E {estimator}"
createScripts("Classification", packagePath, "weka_c_template", "BayesNet", None, BayesNet, {"estimator": ["weka.classifiers.bayes.net.estimate.SimpleEstimator -- -A 0.5", "weka.classifiers.bayes.net.estimate.BayesNetEstimator -A 0.5", "weka.classifiers.bayes.net.estimate.BMAEstimator -A 0.5", "weka.classifiers.bayes.net.estimate.MultiNomialBMAEstimator -k2"], "searchAlgorithm": ["weka.classifiers.bayes.net.search.local.K2 -- -P 1 -S BAYES", "weka.classifiers.bayes.net.search.local.EBMC -T 2 -P 2 -C 2 -S K2", "weka.classifiers.bayes.net.search.local.GeneticSearch -L 10 -A 100 -U 10 -R 1 -M -C -S BAYES", "weka.classifiers.bayes.net.search.local.HillClimber -P 1 -S BAYES", "weka.classifiers.bayes.net.search.local.LAGDHillClimber -L 2 -G 5 -P 1 -S BAYES", "weka.classifiers.bayes.net.search.local.RepeatedHillClimber -U 10 -A 1 -P 1 -S BAYES", "weka.classifiers.bayes.net.search.local.SimulatedAnnealing -A 10.0 -U 10000 -D 0.999 -R 1 -S BAYES", "weka.classifiers.bayes.net.search.local.TabuSearch -L 5 -U 10 -P 1 -S BAYES", "weka.classifiers.bayes.net.search.local.TAN -S BAYES"]})

DecisionTable = 'weka.classifiers.rules.DecisionTable {evaluationMeasure} -X 5 -S "{search}"'
createScripts("Classification", packagePath, "weka_c_template", "DecisionTable", None, DecisionTable, {"evaluationMeasure": ["", "-E auc", "-E rmse"], "search": searchAlgorithms})

HoeffdingTree = "weka.classifiers.trees.HoeffdingTree -L {leafPredictionStrategy} -S {splitCriterion} -E {splitConfidence} -H {hoeffdingTieThreshold} -M {minimumFractionOfWeightInfoGain} -G {gracePeriod} -N {naiveBayesPredictionThreshold}"
createScripts("Classification", packagePath, "weka_c_template", "HoeffdingTree", None, HoeffdingTree, {"gracePeriod": ["100.0", "200.0", "300.0"], "hoeffdingTieThreshold": ["0.02", "0.05", "0.10"], "minimumFractionOfWeightInfoGain": ["0.01"], "splitConfidence": ["1.0E-7"], "splitCriterion": ["1", "0"], "naiveBayesPredictionThreshold": ["0.0"], "leafPredictionStrategy": ["2", "1", "0"]})

HyperPipes = "weka.classifiers.misc.HyperPipes"
createScripts("Classification", packagePath, "weka_c_template", "HyperPipes", None, HyperPipes, {})

# Other option for pruning is -U
J48 = "weka.classifiers.trees.J48 {pruning} {subtreeRaising} {binarySplits} -M {minNumObj} {useMDLcorrection} {collapseTree} {useLaplace}"
createScripts("Classification", packagePath, "weka_c_template", "J48", None, J48, {"pruning": ["-C 0.25", "-U"], "useLaplace": ["", "-A"], "subtreeRaising": ["", "-S"], "binarySplits": ["", "-B"], "minNumObj": ["2"], "useMDLcorrection": ["", "-J"], "collapseTree": ["", "-O"]})

JRip = "weka.classifiers.rules.JRip -F 3 -N {minNo} -O {optimizations} -S 1 -num-decimal-places 7 {checkErrorRate} {usePruning}"
createScripts("Classification", packagePath, "weka_c_template", "JRip", None, JRip, {"minNo": ["2.0"], "optimizations": ["2", "5"], "checkErrorRate": ["", "-E"], "usePruning": ["", "-P"]})

LibLINEAR = "weka.classifiers.functions.LibLINEAR -S {SVMType} -C {cost} -E {eps} -B {bias} -L {epsilonParameter} -I {maximumNumberOfIterations} {normalize}"
createScripts("Classification", packagePath, "weka_c_template", "LibLINEAR", None, LibLINEAR, {"bias": ["1.0", "-1.0"], "eps": ["0.001"], "cost": cOptions, "SVMType": ["1", "2", "3", "4", "5", "6", "7", "11"], "maximumNumberOfIterations": ["1000", "2000"], "normalize": ["", "-Z"], "epsilonParameter": ["0.1"]})

MultilayerPerceptron = "weka.classifiers.functions.MultilayerPerceptron -L {learningRate} -M {momentum} -N {trainingTime} -V {validationSetSize} -S 0 -E {validationThreshold} -H {hiddenLayers} -I {normalizeAttributes} {decay} {reset}"
createScripts("Classification", packagePath, "weka_c_template", "MultilayerPerceptron", None, MultilayerPerceptron, {"momentum": ["0.2", "0.1", "0.3"], "hiddenLayers": ["a", 0, "i", "o", "t"], "validationThreshold": ["20"], "normalizeAttributes": ["", "-I"], "decay": ["", "-D"], "validationSetSize": ["0"], "trainingTime": ["500", "100", "1000"], "learningRate": ["0.3", "0.2", "0.4"], "reset": ["", "-R"]})

NaiveBayes = "weka.classifiers.bayes.NaiveBayes {useKernelEstimator} {useSupervisedDiscretization}"
createScripts("Classification", packagePath, "weka_c_template", "NaiveBayes", None, NaiveBayes, {"useKernelEstimator": ["", "-K"], "useSupervisedDiscretization": [""]})

OneR = "weka.classifiers.rules.OneR -B {minBucketSize}"
createScripts("Classification", packagePath, "weka_c_template", "OneR", None, OneR, {"minBucketSize": ["6", "3", "9"]})

RandomForest = "weka.classifiers.trees.RandomForest -P {bagSizePercent} -I {numIterations} -num-slots 1 -K {numFeatures} -M 1.0 -V 0.001 -S 1 {breakTiesRandomly} {maxDepth} {calcOutOfBag}"
createScripts("Classification", packagePath, "weka_c_template", "RandomForest", None, RandomForest, {"bagSizePercent": ["100"], "numIterations": ["100", "50", "1000"], "breakTiesRandomly": ["", "-B"], "maxDepth": [""], "calcOutOfBag": [""], "numFeatures": ["0", "5", "10"]})

RandomTree = "weka.classifiers.trees.RandomTree -K {KValue} -M {minNum} -V {minVarianceProp} -S 1 {numFolds} {breakTiesRandomly} {maxDepth}"
createScripts("Classification", packagePath, "weka_c_template", "RandomTree", None, RandomTree, {"minNum": ["1.0"], "numFolds": [""], "breakTiesRandomly": ["", "-B"], "maxDepth": [""], "minVarianceProp": ["0.001", "0.01"], "KValue": ["0", "5", "10"]})

RBFNetwork = "weka.classifiers.functions.RBFNetwork -B {numClusters} -S 1 -R {ridge} -M {maxIts} -W {minStdDev}"
createScripts("Classification", packagePath, "weka_c_template", "RBFNetwork", None, RBFNetwork, {"ridge": ["1.0E-8", "1.0E-6", "1.0E-4"], "maxIts": ["-1"], "numClusters": ["2", "3", "6"], "minStdDev": ["0.1", "0.05", "0.2"]})

REPTree = "weka.classifiers.trees.REPTree -M {minNum} -V {minVarianceProp} -N {numFolds} -S 1 -L {maxDepth} -I {initialCount} {noPruning} {spreadInitialCount}"
createScripts("Classification", packagePath, "weka_c_template", "REPTree", None, REPTree, {"minNum": ["2"], "numFolds": ["3"], "noPruning": ["", "-P"], "spreadInitialCount": ["", "-R"], "maxDepth": ["-1"], "minVarianceProp": ["0.001", "0.01"], "initialCount": ["0.0"]})

SimpleLogistic = "weka.classifiers.functions.SimpleLogistic -I 0 -M 500 -H 50 -W {weightTrimBeta} {useAIC}"
createScripts("Classification", packagePath, "weka_c_template", "SimpleLogistic", None, SimpleLogistic, {"useAIC": ["", "-A"], "weightTrimBeta": ["0.0", "0.1", "0.5"]})

SMO = 'weka.classifiers.functions.SMO -C {c} -L 0.001 -P 1.0E-12 -N {filterType} -V {numFolds} -W 1 -K "{kernel}" {buildCalibrationModels} -calibrator "{calibrator}"'
createScripts("Classification", packagePath, "weka_c_template", "SMO", None, SMO, {"buildCalibrationModels": ["", "-M"], "numFolds": ["-1"], "c": cOptions, "kernel": ["weka.classifiers.functions.supportVector.PolyKernel -E 1.0 -C 250007", "weka.classifiers.functions.supportVector.Puk -O 1.0 -S 1.0 -C 250007", "weka.classifiers.functions.supportVector.RBFKernel -G 0.01 -C 250007", "weka.classifiers.functions.supportVector.StringKernel -P 0 -C 250007 -IC 200003 -L 0.5 -ssl 3 -ssl-max 9"], "filterType": ["0", "1", "2"], "calibrator": ["weka.classifiers.functions.Logistic -R 1.0E-8 -M -1 -num-decimal-places 4"]})

LibSVM = "weka.classifiers.functions.LibSVM -S 0 -K {kernelType} -D {degree} -G {gamma} -R {coef0} -N 0.5 -M 40.0 -C {cost} -E {eps} -P {loss} -B -seed 1 {shrinking} {normalize}"
createScripts("Classification", packagePath, "weka_c_template", "LibSVM", None, LibSVM, {"loss": ["0.1"], "kernelType": ["2", "0", "1", "3"], "degree": ["3"], "gamma": ["0.0", "0.1", "0.5"], "shrinking": ["", "-H"], "eps": ["0.001"], "cost": cOptions, "normalize": ["", "-Z"], "coef0": ["0.0"]})

VFI = "weka.classifiers.misc.VFI -B {bias} {weightByConfidence}"
createScripts("Classification", packagePath, "weka_c_template", "VFI", None, VFI, {"bias": ["0.6", "0.3", "0.9"], "weightByConfidence": ["", "-C"]})

ZeroR = "weka.classifiers.rules.ZeroR"
createScripts("Classification", packagePath, "weka_c_template", "ZeroR", None, ZeroR, {})

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

Correlation = 'weka.attributeSelection.CorrelationAttributeEval -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"'
createScripts("FeatureSelection", packagePath, "weka_f_template", "Correlation", None, Correlation, {})

GainRatio = 'weka.attributeSelection.GainRatioAttributeEval -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"'
createScripts("FeatureSelection", packagePath, "weka_f_template", "GainRatio", None, GainRatio, {})

InfoGain = 'weka.attributeSelection.InfoGainAttributeEval -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"'
createScripts("FeatureSelection", packagePath, "weka_f_template", "InfoGain", None, InfoGain, {})

OneR = 'weka.attributeSelection.OneRAttributeEval -S 1 -F {folds} -B {minimumBucketSize} -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"'
createScripts("FeatureSelection", packagePath, "weka_f_template", "OneR", None, OneR, {"folds": ["10"], "minimumBucketSize": ["6"]})

ReliefF = 'weka.attributeSelection.ReliefFAttributeEval -M -1 -D 1 -K {numNeighbors} {weightByDistance} -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"'
createScripts("FeatureSelection", packagePath, "weka_f_template", "ReliefF", None, ReliefF, {"numNeighbors": ["10"], "weightByDistance": [""]})

SVMRFE = 'weka.attributeSelection.SVMAttributeEval -X {attsToEliminatePerIteration} -Y {percentToEliminatePerIteration} -Z {percentThreshold} -P {epsilonParameter} -T {toleranceParameter} -C {complexityParameter} -N {filterType} -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"'
createScripts("FeatureSelection", packagePath, "weka_f_template", "SVMRFE", None, SVMRFE, {"percentThreshold": ["1"], "filterType": ["0"], "toleranceParameter": ["1.0E-10"], "complexityParameter": ["1.0"], "attsToEliminatePerIteration": ["0"], "epsilonParameter": ["1.0E-25"], "percentToEliminatePerIteration": ["10"]})

SymmetricalUncertainty = 'weka.attributeSelection.SymmetricalUncertAttributeEval -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"'
createScripts("FeatureSelection", packagePath, "weka_f_template", "SymmetricalUncertainty", None, SymmetricalUncertainty, {})
