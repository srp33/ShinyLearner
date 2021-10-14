import os, sys
from build_scripts_helper import *

showStats = sys.argv[1] == "True"

summaryDict = {}

#############################################################
# Meta options
#############################################################

packagePath = "tsv/sklearn"

numEstimatorOptions = [50, 1000]
boostAlgorithmOptions = ["SAMME.R", "SAMME"]
bootstrapOptions = [True, False]
oobScoreOptions = [False, True]
treeCriterionOptions = ["gini", "entropy"]
splitterOptions = ["best", "random"]
classWeightOptions = [None, "'balanced'"]
neighborOptions = [1, 5, 10]
weightOptions = ["uniform", "distance"]
pOptions = [1, 2]
cOptions = [1.0, 0.1, 10.0, 100.0]

#############################################################
# Classifiers
#############################################################

adaboost = "clf = AdaBoostClassifier(base_estimator={base_estimator}, n_estimators={n_estimators}, learning_rate=1.0, algorithm='{algorithm}', random_state=R_SEED)"
createScripts("Classification", packagePath, "sklearn_c_template", "adaboost", None, adaboost, {"base_estimator": ["DecisionTreeClassifier()", "LogisticRegression()"], "n_estimators": numEstimatorOptions, "algorithm": boostAlgorithmOptions}, summaryDict)

# The system fails when you use bagging with multiple cores
#bagging = "clf = BaggingClassifier(base_estimator={base_estimator}, n_estimators={n_estimators}, max_samples=1.0, max_features=1.0, bootstrap={bootstrap}, bootstrap_features=False, oob_score={oob_score}, warm_start=False, n_jobs={n_jobs}, random_state=R_SEED, verbose=0)"
#createScripts("Classification", packagePath, "sklearn_c_template", "bagging", None, bagging, {"base_estimator": ["DecisionTreeClassifier()", "LogisticRegression()", "SVC()"], "n_estimators": [50, 100], "bootstrap": bootstrapOptions, "oob_score": oobScoreOptions}, summaryDict, {"bootstrap": False, "oob_score": True})

decision_tree = "clf = DecisionTreeClassifier(criterion='{criterion}', splitter='{splitter}', max_depth={max_depth}, min_samples_split={min_samples_split}, min_samples_leaf={min_samples_leaf}, min_weight_fraction_leaf={min_weight_fraction_leaf}, max_features={max_features}, max_leaf_nodes={max_leaf_nodes}, class_weight={class_weight}, random_state=R_SEED)"
createScripts("Classification", packagePath, "sklearn_c_template", "decision_tree", None, decision_tree, {"criterion": treeCriterionOptions, "splitter": splitterOptions, "max_depth": [None], "min_samples_split": [2, 4], "min_samples_leaf": [1, 3, 5], "min_weight_fraction_leaf": [0.0], "max_features": [None], "max_leaf_nodes": [None, 5], "class_weight": classWeightOptions}, summaryDict)

extra_trees = "clf = ExtraTreesClassifier(n_estimators={n_estimators}, criterion='{criterion}', max_depth={max_depth}, min_samples_split={min_samples_split}, min_samples_leaf={min_samples_leaf}, min_weight_fraction_leaf={min_weight_fraction_leaf}, max_features={max_features}, max_leaf_nodes={max_leaf_nodes}, bootstrap={bootstrap}, oob_score={oob_score}, class_weight={class_weight}, n_jobs={n_jobs}, random_state=R_SEED, verbose=0, warm_start=False)"
createScripts("Classification", packagePath, "sklearn_c_template", "extra_trees", None, extra_trees, {"n_estimators": numEstimatorOptions, "criterion": treeCriterionOptions, "max_depth": [None], "min_samples_split": [2], "min_samples_leaf": [1], "min_weight_fraction_leaf": [0.0], "max_features": [None], "max_leaf_nodes": [None], "bootstrap": bootstrapOptions, "oob_score": oobScoreOptions, "class_weight": classWeightOptions}, summaryDict, {"bootstrap": False, "oob_score": True})

#gaussian_process = "clf = GaussianProcessClassifier(kernel={kernel}, optimizer='fmin_l_bfgs_b', n_restarts_optimizer={n_restarts_optimizer}, max_iter_predict={max_iter_predict}, warm_start=False, copy_X_train=True, random_state=R_SEED, multi_class='one_vs_rest', n_jobs={n_jobs})"
#createScripts("Classification", packagePath, "sklearn_c_template", "gaussian_process", None, gaussian_process, {"kernel": [None, "ConstantKernel()", "DotProduct()", "ExpSineSquared()", "Exponentiation()", "Matern()", "RBF()", "RationalQuadratic()", "WhiteKernel()", "Sum(RBF(), DotProduct())", "Product(RBF(), DotProduct())"], "n_restarts_optimizer": [0, 2, 5], "max_iter_predict": [100, 500, 1000]}, summaryDict)

gradient_boosting = "clf = GradientBoostingClassifier(loss='{loss}', learning_rate=0.1, n_estimators={n_estimators}, subsample=1.0, criterion='{criterion}', min_samples_split={min_samples_split}, min_samples_leaf={min_samples_leaf}, min_weight_fraction_leaf={min_weight_fraction_leaf}, max_depth={max_depth}, init=None, max_features={max_features}, verbose=0, max_leaf_nodes={max_leaf_nodes}, warm_start=False, random_state=R_SEED)"
createScripts("Classification", packagePath, "sklearn_c_template", "gradient_boosting", None, gradient_boosting, {"loss": ['deviance'], "n_estimators": numEstimatorOptions, "criterion": ['friedman_mse', 'mse', 'mae'], "min_samples_split": [2], "min_samples_leaf": [1], "min_weight_fraction_leaf": [0.0], "max_depth": [3], "max_features": [None], "max_leaf_nodes": [None]}, summaryDict)

knn = "clf = KNeighborsClassifier(n_neighbors={n_neighbors}, weights='{weights}', algorithm='auto', leaf_size=30, p={p}, metric='minkowski', metric_params=None, n_jobs={n_jobs})"
createScripts("Classification", packagePath, "sklearn_c_template", "knn", None, knn, {"n_neighbors": neighborOptions, "weights": weightOptions, "p": pOptions}, summaryDict)

lda = "clf = LinearDiscriminantAnalysis(solver='{solver}', shrinkage=None, priors=None, n_components=None, store_covariance=False, tol={tol})"
createScripts("Classification", packagePath, "sklearn_c_template", "lda", None, lda, {"solver": ["svd"], "tol": [0.0001, 0.00001, 0.001]}, summaryDict)

logistic_regression = "clf = LogisticRegression(penalty='{penalty}', dual={dual}, tol={tol}, C={C}, fit_intercept=True, intercept_scaling=1, class_weight={class_weight}, solver='{solver}', max_iter={max_iter}, multi_class='{multi_class}', verbose=0, warm_start=False, n_jobs={n_jobs}, random_state=R_SEED)"
createScripts("Classification", packagePath, "sklearn_c_template", "logistic_regression", None, logistic_regression, {"penalty": ['l2'], "dual": [False], "tol": [0.0001], "C": cOptions, "class_weight": classWeightOptions, "solver": ['liblinear', 'newton-cg', 'lbfgs', 'sag'], "max_iter": [100], "multi_class": ['ovr']}, summaryDict)

multilayer_perceptron = "clf = MLPClassifier(hidden_layer_sizes={hidden_layer_sizes}, activation='{activation}', solver='{solver}', alpha={alpha}, batch_size='auto', learning_rate='{learning_rate}', learning_rate_init=0.001, power_t=0.5, max_iter={max_iter}, shuffle=True, tol={tol}, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True, early_stopping={early_stopping}, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08, random_state=R_SEED)"
createScripts("Classification", packagePath, "sklearn_c_template", "multilayer_perceptron", None, multilayer_perceptron, {"hidden_layer_sizes": [(100, ), (500, )], "activation": ['relu', 'identity', 'logistic', 'tanh'], "solver": ['adam', 'lbfgs', 'sgd'], "alpha": [0.0001], "learning_rate": ['constant'], "max_iter": [200], "tol": [0.0001], "early_stopping": [False]}, summaryDict)

random_forest = "clf = RandomForestClassifier(n_estimators={n_estimators}, criterion='{criterion}', max_depth={max_depth}, min_samples_split={min_samples_split}, min_samples_leaf={min_samples_leaf}, min_weight_fraction_leaf={min_weight_fraction_leaf}, max_features='auto', max_leaf_nodes={max_leaf_nodes}, bootstrap={bootstrap}, oob_score={oob_score}, n_jobs={n_jobs}, verbose=0, warm_start=False, class_weight={class_weight}, random_state=R_SEED)"
createScripts("Classification", packagePath, "sklearn_c_template", "random_forest", None, random_forest, {"n_estimators": numEstimatorOptions, "criterion": treeCriterionOptions, "max_depth": [None], "min_samples_split": [2], "min_samples_leaf": [1], "min_weight_fraction_leaf": [0.0], "max_leaf_nodes": [None], "bootstrap": bootstrapOptions, "oob_score": oobScoreOptions, "class_weight": classWeightOptions}, summaryDict, {"bootstrap": False, "oob_score": True})

sgd = "clf = SGDClassifier(loss='modified_huber', penalty='{penalty}', alpha={alpha}, l1_ratio=0.15, fit_intercept=True, early_stopping={early_stopping}, shuffle=True, verbose=0, epsilon={epsilon}, n_jobs={n_jobs}, learning_rate='{learning_rate}', eta0=0.0, power_t=0.5, class_weight={class_weight}, warm_start=False, average=False, random_state=R_SEED)"
#loss='modified_huber' is required for probabilistic predictions
createScripts("Classification", packagePath, "sklearn_c_template", "sgd", None, sgd, {"penalty": ['l2', 'l1', 'elasticnet'], "alpha": [0.0001, 0.00001, 0.001], "epsilon": [0.1], "learning_rate": ['optimal', 'constant', 'invscaling', 'adaptive'], "early_stopping": [False, True], "class_weight": classWeightOptions}, summaryDict)

svm = "clf = SVC(C={C}, kernel='{kernel}', degree=3, gamma='auto', coef0=0.0, shrinking={shrinking}, tol={tol}, cache_size=200, class_weight={class_weight}, verbose=False, max_iter=-1, decision_function_shape='ovr', probability=True, random_state=R_SEED)"
createScripts("Classification", packagePath, "sklearn_c_template", "svm", None, svm, {"C": cOptions, "kernel": ['rbf', 'linear', 'poly', 'sigmoid'], "shrinking": [True], "tol": [0.001], "class_weight": classWeightOptions}, summaryDict)

#nu_svc = "clf = NuSVC(nu={nu}, kernel='{kernel}', degree=3, gamma='auto', coef0=0.0, shrinking={shrinking}, probability=True, tol={tol}, cache_size=200, class_weight={class_weight}, verbose=False, max_iter=-1, decision_function_shape='ovr', random_state=R_SEED)"
#createScripts("Classification", packagePath, "sklearn_c_template", "nu_svc", None, nu_svc, {"nu": [0.5, 0.1, 0.25, 0.75, 0.9], "kernel": ['rbf', 'linear', 'poly', 'sigmoid'], "shrinking": [True, False], "tol": [0.001], "class_weight": classWeightOptions}, summaryDict)

## Failed tests: gaussian_naivebayes gaussian_process qda

#############################################################
# Feature selectors
#############################################################

anova = "F, score = f_classif(train_X, train_y)"
createScripts("FeatureSelection", packagePath, "sklearn_f_template", "anova", "score", anova, {}, summaryDict)

mutual_info = "score = 1 - mutual_info_classif(train_X, train_y, n_neighbors={n_neighbors})"
createScripts("FeatureSelection", packagePath, "sklearn_f_template", "mutual_info", "score", mutual_info, {"n_neighbors": [3, 1, 5, 10]}, summaryDict)

random_forest_rfe = "selector = RFE(RandomForestClassifier(n_estimators=100, random_state=R_SEED), n_features_to_select=1, step={step})"
createScripts("FeatureSelection", packagePath, "sklearn_f_template", "random_forest_rfe", "rfe", random_forest_rfe, {"step": [0.1, 0.02, 0.05, 0.2]}, summaryDict)

#random_logistic_regression = "scorer = RandomizedLogisticRegression(C={C}, scaling={scaling}, sample_fraction={sample_fraction}, n_resampling={n_resampling}, selection_threshold={selection_threshold}, tol={tol}, fit_intercept=True, verbose=False, normalize=True, random_state=R_SEED)"
#createScripts("FeatureSelection", packagePath, "sklearn_f_template", "random_logistic_regression", "coef", random_logistic_regression, {"C": [1], "scaling": [0.5], "sample_fraction": [0.75], "n_resampling": [200], "selection_threshold": [0.25], "tol": [0.001]}, summaryDict)

svm_rfe = "selector = RFE(SVC(random_state=R_SEED, kernel='linear'), n_features_to_select=1, step={step})"
createScripts("FeatureSelection", packagePath, "sklearn_f_template", "svm_rfe", "rfe", svm_rfe, {"step": [0.1, 0.02, 0.05, 0.2]}, summaryDict)

##svm_wrapper = "wrapper = SequentialFeatureSelector(SVC(random_state=R_SEED, kernel='rbf'), n_features_to_select=3, direction='forward')"
##createScripts("FeatureSelection", packagePath, "sklearn_f_template", "svm_wrapper", "wrapper", svm_wrapper, {}, summaryDict)

##logistic_wrapper = "wrapper = SequentialFeatureSelector(LogisticRegression(penalty='l2', dual=False, tol=0.0001, C=1.0, fit_intercept=True, intercept_scaling=1, class_weight=None, solver='liblinear', max_iter=100, multi_class='ovr', verbose=0, warm_start=False, n_jobs={n_jobs}, random_state=R_SEED), n_features_to_select=1, direction='forward')"
##createScripts("FeatureSelection", packagePath, "sklearn_f_template", "logistic_wrapper", "wrapper", logistic_wrapper, {}, summaryDict)

##mlp_wrapper = "wrapper = SequentialFeatureSelector(MLPClassifier(hidden_layer_sizes=(100,), activation='relu', solver='adam', alpha=0.0001, batch_size='auto', learning_rate='constant', learning_rate_init=0.001, power_t=0.5, max_iter=200, shuffle=True, tol=0.0001, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True, early_stopping=False, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-08, random_state=R_SEED), n_features_to_select=1, direction='forward')"
##createScripts("FeatureSelection", packagePath, "sklearn_f_template", "mlp_wrapper", "wrapper", mlp_wrapper, {}, summaryDict)

##rf_wrapper = "wrapper = SequentialFeatureSelector(RandomForestClassifier(n_estimators=50, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=None, bootstrap=True,oob_score=False, n_jobs={n_jobs}, verbose=0, warm_start=False, class_weight=None, random_state=R_SEED), n_features_to_select=1, direction='forward')"
##createScripts("FeatureSelection", packagePath, "sklearn_f_template", "rf_wrapper", "wrapper", rf_wrapper, {}, summaryDict)

##knn_wrapper = "wrapper = SequentialFeatureSelector(KNeighborsClassifier(n_neighbors=1, weights='uniform', algorithm='auto', leaf_size=30, p=1, metric='minkowski', metric_params=None, n_jobs={n_jobs}), n_features_to_select=1, direction='forward')"
##createScripts("FeatureSelection", packagePath, "sklearn_f_template", "knn_wrapper", "wrapper", knn_wrapper, {}, summaryDict)

## Failed tests: random_lasso

if showStats:
    print("#######################################")
    for key, value in sorted(summaryDict.items()):
        print(key, value)
    print("#######################################")
    print("Total: {}".format(sum(summaryDict.values())))
    print("#######################################")
