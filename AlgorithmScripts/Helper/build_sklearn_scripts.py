import os, sys, shutil

def createScript(algorithmType, templateFilePath, shortAlgName, algFileName, algInstantiation):
    scriptDir = "../{}/tsv/sklearn/{}".format(algorithmType, shortAlgName)
    if not os.path.exists(scriptDir):
        os.makedirs(scriptDir, exist_ok=True)

    destFilePath = "{}/{}".format(scriptDir, algFileName)
    print("Saving to {}.".format(destFilePath))

    # Copy the file first to preserve permissions
    shutil.copy(templateFilePath, destFilePath)

    with open(destFilePath) as templateFile:
        template = templateFile.read()
        template = template.replace("{algorithmInstantiation}", algInstantiation)

    with open(destFilePath, 'w') as destFile:
        destFile.write(template)

createScript("Classification", "sklearn_c_template", "adaboost", "default",
    "from sklearn.ensemble import AdaBoostClassifier; " +
    "clf = AdaBoostClassifier(n_estimators=50, random_state=R_SEED)")
createScript("Classification", "sklearn_c_template", "bagging", "default",
    "from sklearn.ensemble import BaggingClassifier; " +
    "clf = BaggingClassifier(n_estimators=50, random_state=R_SEED)")
createScript("Classification", "sklearn_c_template", "decision_tree", "default",
    "from sklearn.tree import DecisionTreeClassifier; " +
    "clf = DecisionTreeClassifier(random_state=R_SEED)")
createScript("Classification", "sklearn_c_template", "extra_trees", "default",
    "from sklearn.ensemble import ExtraTreesClassifier; " +
    "clf = ExtraTreesClassifier(n_estimators=50, random_state=R_SEED)")
createScript("Classification", "sklearn_c_template", "gradient_boosting", "default",
    "from sklearn.ensemble import GradientBoostingClassifier; " +
    "clf = GradientBoostingClassifier(n_estimators=50, random_state=R_SEED)")
createScript("Classification", "sklearn_c_template", "knn", "default",
    "from sklearn.neighbors import KNeighborsClassifier; "
    "clf = KNeighborsClassifier()")
createScript("Classification", "sklearn_c_template", "lda", "default",
    "from sklearn.discriminant_analysis import LinearDiscriminantAnalysis; " +
    "clf = LinearDiscriminantAnalysis()")
createScript("Classification", "sklearn_c_template", "logistic_regression", "default",
    "from sklearn.linear_model import LogisticRegression; " +
    "clf = LogisticRegression(random_state=R_SEED)")
createScript("Classification", "sklearn_c_template", "multilayer_perceptron", "default",
    "from sklearn.neural_network import MLPClassifier; "
    "clf = MLPClassifier(random_state=R_SEED)")
createScript("Classification", "sklearn_c_template", "random_forest", "default",
    "from sklearn.ensemble import RandomForestClassifier; " +
    "clf = RandomForestClassifier(n_estimators=50, random_state=R_SEED)")
createScript("Classification", "sklearn_c_template", "sgd", "default",
    "from sklearn.linear_model import SGDClassifier; " +
    "clf = SGDClassifier(random_state=R_SEED, loss='modified_huber')") # It is necessary to use this loss function with sgd to produce probabilistic predictions
createScript("Classification", "sklearn_c_template", "svm", "default",
    "from sklearn.svm import SVC; " +
    "clf = SVC(probability=True, random_state=R_SEED)")

createScript("FeatureSelection", "sklearn_f_template", "anova", "default",
    "from sklearn.feature_selection import f_classif; " +
    "F, pval = f_classif(train_X, train_y); " +
    "random_array = random.random(len(pval)); " +
    "order = lexsort((random_array,pval)); " +
    "rankedFeatures = [features[i] for i in order]")
createScript("FeatureSelection", "sklearn_f_template", "mutual_info", "default",
    "from sklearn.feature_selection import mutual_info_classif; " +
    "pval = 1 - mutual_info_classif(train_X, train_y); " +
    "random_array = random.random(len(pval)); " +
    "order = lexsort((random_array,pval)); " +
    "rankedFeatures = [features[i] for i in order]")
createScript("FeatureSelection", "sklearn_f_template", "random_forest_rfe", "default",
    "from sklearn.ensemble import RandomForestClassifier; " +
    "from sklearn.feature_selection import RFE; " +
    "estimator = RandomForestClassifier(n_estimators=50, random_state=R_SEED); " +
    "selector = RFE(estimator, n_features_to_select=5, step=0.1); " +
    "selector.fit(train_X, train_y); " +
    "rankedFeatures = [y[1] for y in sorted(zip(map(lambda x: round(x, 4), selector.ranking_), features))]")
createScript("FeatureSelection", "sklearn_f_template", "random_logistic_regression", "default",
    "from sklearn.linear_model import RandomizedLogisticRegression; " +
    "scorer = RandomizedLogisticRegression(random_state=R_SEED); " +
    "scorer.fit(train_X, train_y); " +
    "rankedFeatures = [y[1] for y in sorted(zip(map(lambda x: round(x, 4), scorer.scores_), features), reverse=True)]")
createScript("FeatureSelection", "sklearn_f_template", "svm_rfe", "default",
    "from sklearn.svm import SVC; " +
    "from sklearn.feature_selection import RFE; " +
    "estimator = SVC(random_state=R_SEED, kernel='linear'); " +
    "selector = RFE(estimator, n_features_to_select=5, step=0.1); " +
    "selector.fit(train_X, train_y); rankedFeatures = [y[1] for y in sorted(zip(map(lambda x: round(x, 4), selector.ranking_), features))]")

## Failed (classification): gaussian_naivebayes gaussian_process qda
## Failed (feature selection): random_lasso
