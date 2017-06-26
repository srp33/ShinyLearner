import os, sys, shutil

def createScript(algorithmType, templateFilePath, shortAlgName, algFileName, algorithm):
    scriptDir = "../{}/arff/weka/{}".format(algorithmType, shortAlgName)
    if not os.path.exists(scriptDir):
        os.makedirs(scriptDir, exist_ok=True)

    destFilePath = "{}/{}".format(scriptDir, algFileName)
    print("Saving to {}.".format(destFilePath))

    # Copy the file first to preserve permissions
    shutil.copy(templateFilePath, destFilePath)

    with open(destFilePath) as templateFile:
        template = templateFile.read()
        template = template.replace("{algorithm}", algorithm)

    with open(destFilePath, 'w') as destFile:
        destFile.write(template)

### The default is ZeroR. Don't use DecisionStump though because not super accurate.
###createScript("Classification, "weka_c_template", AdaBoostM1 "weka.classifiers.meta.AdaBoostM1 -P 100 -S 1 -I 10 -W weka.classifiers.trees.DecisionStump"
createScript("Classification", "weka_c_template", "Bagging", "default", "weka.classifiers.meta.Bagging -P 100 -S 1 -num-slots 1 -I 10 -W weka.classifiers.trees.REPTree -- -M 2 -V 0.001 -N 3 -S 1 -L -1 -I 0.0")
createScript("Classification", "weka_c_template", "BayesNet", "default", "weka.classifiers.bayes.BayesNet -D -Q weka.classifiers.bayes.net.search.local.K2 -- -P 1 -S BAYES -E weka.classifiers.bayes.net.estimate.SimpleEstimator -- -A 0.5")
createScript("Classification", "weka_c_template", "DecisionTable", "default", 'weka.classifiers.rules.DecisionTable -X 1 -S "weka.attributeSelection.BestFirst -D 1 -N 5"')
createScript("Classification", "weka_c_template", "HoeffdingTree", "default", "weka.classifiers.trees.HoeffdingTree -L 2 -S 1 -E 1.0E-7 -H 0.05 -M 0.01 -G 200.0 -N 0.0")
createScript("Classification", "weka_c_template", "HyperPipes", "default", "weka.classifiers.misc.HyperPipes")
### Probably can use this one but not accurate enough with the default settings
##createScript("Classification", "weka_c_template", "IBk", "default", 'weka.classifiers.lazy.IBk -K 1 -W 0 -A "weka.core.neighboursearch.LinearNNSearch -A \"weka.core.EuclideanDistance -R first-last\""')
createScript("Classification", "weka_c_template", "J48", "default", "weka.classifiers.trees.J48 -C 0.25 -M 2")
createScript("Classification", "weka_c_template", "JRip", "default", "weka.classifiers.rules.JRip -F 3 -N 2.0 -O 2 -S 1 -num-decimal-places 7")
createScript("Classification", "weka_c_template", "LibLINEAR", "default", "weka.classifiers.functions.LibLINEAR -S 1 -C 1.0 -E 0.001 -B 1.0 -L 0.1 -I 1000")
### The default is ZeroR. Don't use DecisionStump though because not super accurate.
###createScript("Classification", "weka_c_template", "LogitBoost_DecisionStump", "default", "weka.classifiers.meta.LogitBoost -P 100 -L -1.7976931348623157E308 -H 1.0 -Z 3.0 -O 1 -E 1 -S 1 -I 10 -W weka.classifiers.trees.DecisionStump -batch-size")
### The default is ZeroR. Don't use DecisionStump though because not super accurate.
###createScript("Classification", "weka_c_template", "LWL", "default", 'weka.classifiers.lazy.LWL -U 0 -K -1 -A "weka.core.neighboursearch.LinearNNSearch -A \"weka.core.EuclideanDistance -R first-last\"" -W weka.classifiers.trees.DecisionStump')
createScript("Classification", "weka_c_template", "MultilayerPerceptron", "default", "weka.classifiers.functions.MultilayerPerceptron -L 0.3 -M 0.2 -N 500 -V 0 -S 0 -E 20 -H a -I")
createScript("Classification", "weka_c_template", "NaiveBayes", "default", "weka.classifiers.bayes.NaiveBayes")
createScript("Classification", "weka_c_template", "OneR", "default", "weka.classifiers.rules.OneR -B 6")
createScript("Classification", "weka_c_template", "RandomForest", "default", "weka.classifiers.trees.RandomForest -I 100 -K 0 -S 1")
createScript("Classification", "weka_c_template", "RandomTree", "default", "weka.classifiers.meta.RandomCommittee -S 1 -I 10 -W weka.classifiers.trees.RandomTree -- -K 0 -M 1.0 -S 1")
createScript("Classification", "weka_c_template", "RBFNetwork", "default", "weka.classifiers.functions.RBFNetwork -B 2 -S 1 -R 1.0E-8 -M -1 -W 0.1")
createScript("Classification", "weka_c_template", "REPTree", "default", "weka.classifiers.meta.RandomSubSpace -P 0.5 -S 1 -I 10 -W weka.classifiers.trees.REPTree -- -M 2 -V 0.001 -N 3 -S 1 -L -1")
createScript("Classification", "weka_c_template", "SimpleLogistic", "default", "weka.classifiers.functions.SimpleLogistic -I 0 -M 500 -H 50 -W 0.0")
createScript("Classification", "weka_c_template", "SMO", "default", 'weka.classifiers.functions.SMO -C 1.0 -L 0.001 -P 1.0E-12 -N 2 -V -1 -W 1 -K "weka.classifiers.functions.supportVector.PolyKernel -E 1.0 -C 250007" -calibrator "weka.classifiers.functions.Logistic -R 1.0E-8 -M -1 -num-decimal-places 4"')
createScript("Classification", "weka_c_template", "SVM", "default", "weka.classifiers.functions.LibSVM -S 0 -K 2 -D 3 -G 0.0 -R 0.0 -N 0.5 -M 40.0 -C 1.0 -E 0.001 -P 0.1 -B -seed 1")
#createScript("Classification", "weka_c_template", "SVM_Linear", "default", "weka.classifiers.functions.LibSVM -S 0 -K 0 -D 3 -G 0.0 -R 0.0 -N 0.5 -M 40.0 -C 1.0 -E 0.001 -P 0.1 -B")
#createScript("Classification", "weka_c_template", "SVM_Poly", "default", "weka.classifiers.functions.LibSVM -S 0 -K 1 -D 3 -G 0.0 -R 0.0 -N 0.5 -M 40.0 -C 1.0 -E 0.0010 -P 0.1 -B")
#createScript("Classification", "weka_c_template", "SVM_RBF", "default", "weka.classifiers.functions.LibSVM -S 0 -K 2 -D 3 -G 0.0 -R 0.0 -N 0.5 -M 40.0 -C 1.0 -E 0.0010 -P 0.1 -B")
createScript("Classification", "weka_c_template", "VFI", "default", "weka.classifiers.misc.VFI -B 0.6")
createScript("Classification", "weka_c_template", "ZeroR", "default", "weka.classifiers.rules.ZeroR")

createScript("FeatureSelection", "weka_f_template", "Correlation", "default", 'weka.attributeSelection.CorrelationAttributeEval -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"')
createScript("FeatureSelection", "weka_f_template", "GainRatio", "default", 'weka.attributeSelection.GainRatioAttributeEval -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"' "")
createScript("FeatureSelection", "weka_f_template", "InfoGain", "default", 'weka.attributeSelection.InfoGainAttributeEval -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"')
createScript("FeatureSelection", "weka_f_template", "OneR", "default", 'weka.attributeSelection.OneRAttributeEval -S 1 -F 10 -B 6 -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"')
createScript("FeatureSelection", "weka_f_template", "ReliefF", "default", 'weka.attributeSelection.ReliefFAttributeEval -M -1 -D 1 -K 10 -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"')
createScript("FeatureSelection", "weka_f_template", "SVMRFE", "default", 'weka.attributeSelection.SVMAttributeEval -X 1 -Y 10 -Z 1 -P 1.0E-25 -T 1.0E-10 -C 1.0 -N 0 -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"')
createScript("FeatureSelection", "weka_f_template", "SymetricalUncertainty", "default", 'weka.attributeSelection.SymmetricalUncertAttributeEval -s \"weka.attributeSelection.Ranker -T -1.7976931348623157E308 -N -1\"')
