import os, sys, shutil

def createScript(algorithmType, templateFilePath, shortAlgName, algFileName, algClass, algInstantiation):
    scriptDir = "../{}/tsv/sklearn/{}".format(algorithmType, shortAlgName)
    if not os.path.exists(scriptDir):
        os.makedirs(scriptDir, exist_ok=True)

    destFilePath = "{}/{}".format(scriptDir, algFileName)
    print("Saving to {}.".format(destFilePath))

    # Copy the file first to preserve permissions
    shutil.copy(templateFilePath, destFilePath)

    with open(destFilePath) as templateFile:
        template = templateFile.read()

        if algClass != None:
            template = template.replace("{algorithmClass}", algClass)

        template = template.replace("{algorithmInstantiation}", algInstantiation)

    with open(destFilePath, 'w') as destFile:
        destFile.write(template)

createScript("Classification", "sklearn_c_template", "adaboost", "default", None,
    "from sklearn.ensemble import AdaBoostClassifier; " +
    "clf = AdaBoostClassifier(n_estimators=50, random_state=R_SEED)")
createScript("Classification", "sklearn_c_template", "bagging", "default", None,
    "from sklearn.ensemble import BaggingClassifier; " +
    "clf = BaggingClassifier(n_estimators=50, random_state=R_SEED)")
createScript("Classification", "sklearn_c_template", "decision_tree", "default", None,
    "from sklearn.tree import DecisionTreeClassifier; " +
    "clf = DecisionTreeClassifier(random_state=R_SEED)")
createScript("Classification", "sklearn_c_template", "extra_trees", "default", None,
    "from sklearn.ensemble import ExtraTreesClassifier; " +
    "clf = ExtraTreesClassifier(n_estimators=50, random_state=R_SEED)")
createScript("Classification", "sklearn_c_template", "gradient_boosting", "default", None,
    "from sklearn.ensemble import GradientBoostingClassifier; " +
    "clf = GradientBoostingClassifier(n_estimators=50, random_state=R_SEED)")
createScript("Classification", "sklearn_c_template", "knn", "default", None,
    "from sklearn.neighbors import KNeighborsClassifier; "
    "clf = KNeighborsClassifier()")
createScript("Classification", "sklearn_c_template", "lda", "default", None,
    "from sklearn.discriminant_analysis import LinearDiscriminantAnalysis; " +
    "clf = LinearDiscriminantAnalysis()")
createScript("Classification", "sklearn_c_template", "logistic_regression", "default", None,
    "from sklearn.linear_model import LogisticRegression; " +
    "clf = LogisticRegression(random_state=R_SEED)")
createScript("Classification", "sklearn_c_template", "multilayer_perceptron", "default", None,
    "from sklearn.neural_network import MLPClassifier; "
    "clf = MLPClassifier(random_state=R_SEED)")
createScript("Classification", "sklearn_c_template", "random_forest", "default", None,
    "from sklearn.ensemble import RandomForestClassifier; " +
    "clf = RandomForestClassifier(n_estimators=50, random_state=R_SEED)")
createScript("Classification", "sklearn_c_template", "sgd", "default", None,
    "from sklearn.linear_model import SGDClassifier; " +
    "clf = SGDClassifier(random_state=R_SEED, loss='modified_huber')") # It is necessary to use this loss function with sgd to produce probabilistic predictions
createScript("Classification", "sklearn_c_template", "svm", "default", None,
    "from sklearn.svm import SVC; " +
    "clf = SVC(probability=True, random_state=R_SEED)")

createScript("FeatureSelection", "sklearn_f_template", "anova", "default", "score",
    "from sklearn.feature_selection import f_classif; " +
    "F, score = f_classif(train_X, train_y)")
createScript("FeatureSelection", "sklearn_f_template", "mutual_info", "default", "score",
    "from sklearn.feature_selection import mutual_info_classif; " +
    "score = 1 - mutual_info_classif(train_X, train_y)")
createScript("FeatureSelection", "sklearn_f_template", "random_forest_rfe", "default", "rfe",
    "from sklearn.ensemble import RandomForestClassifier; " +
    "from sklearn.feature_selection import RFE; " +
    "estimator = RandomForestClassifier(n_estimators=50, random_state=R_SEED)")
createScript("FeatureSelection", "sklearn_f_template", "random_logistic_regression", "default", "coef",
    "from sklearn.linear_model import RandomizedLogisticRegression; " +
    "scorer = RandomizedLogisticRegression(random_state=R_SEED)")
createScript("FeatureSelection", "sklearn_f_template", "svm_rfe", "default", "rfe",
    "from sklearn.svm import SVC; " +
    "from sklearn.feature_selection import RFE; " +
    "estimator = SVC(random_state=R_SEED, kernel='linear')")

## Failed (classification): gaussian_naivebayes gaussian_process qda
## Failed (feature selection): random_lasso
