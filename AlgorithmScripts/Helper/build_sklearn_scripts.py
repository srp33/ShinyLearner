import os, sys, shutil

def createScript(algorithmType, templateFilePath, shortAlgName, algFileName, algClass, paramDict):
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

        algInstantiation = replaceTokens(globals()[shortAlgName], paramDict, shortAlgName)
        template = template.replace("{algorithmInstantiation}", algInstantiation)

    with open(destFilePath, 'w') as destFile:
        destFile.write(template)

def replaceTokens(instantiation, paramDict, shortAlgName):
    for key, value in paramDict.items():
        if "{" + key + "}" not in instantiation:
            print("A key of {} was not found in the algorithm template for {}.".format(key, shortAlgName))
            sys.exit(1)
        instantiation = instantiation.replace("{" + key + "}", str(value))

    return instantiation

adaboost = "clf = AdaBoostClassifier(base_estimator={base_estimator}, n_estimators={n_estimators}, learning_rate=1.0, algorithm='{algorithm}', random_state=R_SEED)"
bagging = "clf = BaggingClassifier(base_estimator={base_estimator}, n_estimators={n_estimators}, max_samples=1.0, max_features=1.0, bootstrap={bootstrap}, bootstrap_features=False, oob_score={oob_score}, warm_start=False, n_jobs=1, random_state=R_SEED, verbose=0)"
decision_tree = "clf = DecisionTreeClassifier(criterion='{criterion}', splitter='{splitter}', max_depth={max_depth}, min_samples_split={min_samples_split}, min_samples_leaf={min_samples_leaf}, min_weight_fraction_leaf={min_weight_fraction_leaf}, max_features={max_features}, max_leaf_nodes={max_leaf_nodes}, min_impurity_split={min_impurity_split}, class_weight={class_weight}, presort=False, random_state=R_SEED)"
extra_trees = "clf = ExtraTreesClassifier(n_estimators={n_estimators}, criterion='{criterion}', max_depth={max_depth}, min_samples_split={min_samples_split}, min_samples_leaf={min_samples_leaf}, min_weight_fraction_leaf={min_weight_fraction_leaf}, max_features={max_features}, max_leaf_nodes={max_leaf_nodes}, min_impurity_split={min_impurity_split}, bootstrap={bootstrap}, oob_score={oob_score}, class_weight={class_weight}, n_jobs=1, random_state=R_SEED, verbose=0, warm_start=False)"
gradient_boosting = "clf = GradientBoostingClassifier(loss='{loss}', learning_rate=0.1, n_estimators={n_estimators}, subsample=1.0, criterion='{criterion}', min_samples_split={min_samples_split}, min_samples_leaf={min_samples_leaf}, min_weight_fraction_leaf={min_weight_fraction_leaf}, max_depth={max_depth}, min_impurity_split={min_impurity_split}, init=None, max_features={max_features}, verbose=0, max_leaf_nodes={max_leaf_nodes}, warm_start=False, presort='auto', random_state=R_SEED)"
knn = "clf = KNeighborsClassifier(n_neighbors={n_neighbors}, weights='{weights}', algorithm='auto', leaf_size={leaf_size}, p={p}, metric='minkowski', metric_params=None, n_jobs=1)"
lda = "clf = LinearDiscriminantAnalysis(solver='{solver}', shrinkage=None, priors=None, n_components=None, store_covariance=False, tol={tol})"
logistic_regression = "clf = LogisticRegression(penalty='{penalty}', dual={dual}, tol={tol}, C={C}, fit_intercept=True, intercept_scaling=1, class_weight={class_weight}, solver='{solver}', max_iter={max_iter}, multi_class='{multi_class}', verbose=0, warm_start=False, n_jobs=1, random_state=R_SEED)"
multilayer_perceptron = "clf = MLPClassifier(hidden_layer_sizes={hidden_layer_sizes}, activation='{activation}', solver='{solver}', alpha={alpha}, batch_size='auto', learning_rate='{learning_rate}', learning_rate_init=0.001, power_t=0.5, max_iter={max_iter}, shuffle=True, tol={tol}, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True, early_stopping={early_stopping}, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08, random_state=R_SEED)"
random_forest = "clf = RandomForestClassifier(n_estimators={n_estimators}, criterion='{criterion}', max_depth={max_depth}, min_samples_split={min_samples_split}, min_samples_leaf={min_samples_leaf}, min_weight_fraction_leaf={min_weight_fraction_leaf}, max_features='auto', max_leaf_nodes={max_leaf_nodes}, min_impurity_split={min_impurity_split}, bootstrap={bootstrap}, oob_score={oob_score}, n_jobs=1, verbose=0, warm_start=False, class_weight={class_weight}, random_state=R_SEED)"
#loss='modified_huber' is required for probabilistic predictions
sgd = "clf = SGDClassifier(loss='modified_huber', penalty='{penalty}', alpha={alpha}, l1_ratio=0.15, fit_intercept=True, n_iter={n_iter}, shuffle=True, verbose=0, epsilon={epsilon}, n_jobs=1, learning_rate='{learning_rate}', eta0=0.0, power_t=0.5, class_weight={class_weight}, warm_start=False, average=False, random_state=R_SEED)"
svm = "clf = SVC(C={C}, kernel='{kernel}', degree=3, gamma='auto', coef0=0.0, shrinking={shrinking}, tol={tol}, cache_size=200, class_weight={class_weight}, verbose=False, max_iter=-1, decision_function_shape='ovr', probability=True, random_state=R_SEED)"

createScript("Classification", "sklearn_c_template", "adaboost", "default", None, {"base_estimator":"None", "n_estimators": 50, "algorithm": "SAMME.R"})
createScript("Classification", "sklearn_c_template", "bagging", "default", None, {"base_estimator":"None", "n_estimators": 50, "bootstrap": True, "oob_score": False})
createScript("Classification", "sklearn_c_template", "decision_tree", "default", None, {"criterion": "gini", "splitter": "best", "max_depth": None, "min_samples_split": 2, "min_samples_leaf": 1, "min_weight_fraction_leaf": 0.0, "max_features": None, "max_leaf_nodes": None, "min_impurity_split": 1e-07, "class_weight": None})
createScript("Classification", "sklearn_c_template", "extra_trees", "default", None, {"n_estimators": 50, "criterion": "gini", "max_depth": None, "min_samples_split": 2, "min_samples_leaf": 1, "min_weight_fraction_leaf": 0.0, "max_features": None, "max_leaf_nodes": None, "min_impurity_split": 1e-07, "bootstrap": False, "oob_score": False, "class_weight": None})
createScript("Classification", "sklearn_c_template", "gradient_boosting", "default", None, {"loss": 'deviance', "n_estimators": 100, "criterion": 'friedman_mse', "min_samples_split": 2, "min_samples_leaf": 1, "min_weight_fraction_leaf": 0.0, "max_depth": 3, "min_impurity_split": 1e-07, "max_features": None, "max_leaf_nodes": None})
createScript("Classification", "sklearn_c_template", "knn", "default", None, {"n_neighbors": 5, "weights": 'uniform', "leaf_size": 30, "p": 2})
createScript("Classification", "sklearn_c_template", "lda", "default", None, {"solver": "svd", "tol": 0.0001})
createScript("Classification", "sklearn_c_template", "logistic_regression", "default", None, {"penalty": 'l2', "dual": False, "tol": 0.0001, "C": 1.0, "class_weight": None, "solver": 'liblinear', "max_iter": 100, "multi_class": 'ovr'})
createScript("Classification", "sklearn_c_template", "multilayer_perceptron", "default", None, {"hidden_layer_sizes": (100, ), "activation": 'relu', "solver": 'adam', "alpha": 0.0001, "learning_rate": 'constant', "max_iter": 200, "tol": 0.0001, "early_stopping": False})
createScript("Classification", "sklearn_c_template", "random_forest", "default", None, {"n_estimators": 50, "criterion": 'gini', "max_depth": None, "min_samples_split": 2, "min_samples_leaf": 1, "min_weight_fraction_leaf": 0.0, "max_leaf_nodes": None, "min_impurity_split": 1e-07, "bootstrap": True, "oob_score": False, "class_weight": None})
createScript("Classification", "sklearn_c_template", "sgd", "default", None, {"penalty": 'l2', "alpha": 0.0001, "n_iter": 5, "epsilon": 0.1, "learning_rate": 'optimal', "class_weight": None})
createScript("Classification", "sklearn_c_template", "svm", "default", None, {"C": 1.0, "kernel": 'rbf', "shrinking": True, "tol": 0.001, "class_weight": None})

anova = "F, score = f_classif(train_X, train_y)"
mutual_info = "score = 1 - mutual_info_classif(train_X, train_y, n_neighbors={n_neighbors})"
random_forest_rfe = "selector = RFE(RandomForestClassifier(n_estimators=50, random_state=R_SEED), n_features_to_select=1, step={step})"
random_logistic_regression = "scorer = RandomizedLogisticRegression(C={C}, scaling={scaling}, sample_fraction={sample_fraction}, n_resampling={n_resampling}, selection_threshold={selection_threshold}, tol={tol}, fit_intercept=True, verbose=False, normalize=True, random_state=R_SEED)"
svm_rfe = "selector = RFE(SVC(random_state=R_SEED, kernel='linear'), n_features_to_select=1, step={step})"

createScript("FeatureSelection", "sklearn_f_template", "anova", "default", "score", {})
createScript("FeatureSelection", "sklearn_f_template", "mutual_info", "default", "score", {"n_neighbors": 3})
createScript("FeatureSelection", "sklearn_f_template", "random_forest_rfe", "default", "rfe", {"step": 0.1})
createScript("FeatureSelection", "sklearn_f_template", "random_logistic_regression", "default", "coef", {"C": 1, "scaling": 0.5, "sample_fraction": 0.75, "n_resampling": 200, "selection_threshold": 0.25, "tol": 0.001})
createScript("FeatureSelection", "sklearn_f_template", "svm_rfe", "default", "rfe", {"step": 0.1})

## Failed (classification): gaussian_naivebayes gaussian_process qda
## Failed (feature selection): random_lasso
