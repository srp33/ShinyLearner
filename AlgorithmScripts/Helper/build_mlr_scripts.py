import os, sys, shutil

def createScript(algorithmType, templateFilePath, shortAlgName, algFileName, params):
    scriptDir = "../{}/tsv/mlr/{}".format(algorithmType, shortAlgName)
    if not os.path.exists(scriptDir):
        os.makedirs(scriptDir, exist_ok=True)

    destFilePath = "{}/{}".format(scriptDir, algFileName)
    print("Saving to {}.".format(destFilePath))

    # Copy the file first to preserve permissions
    shutil.copy(templateFilePath, destFilePath)

    with open(destFilePath) as templateFile:
        template = templateFile.read()
        template = template.replace("{algorithm}", shortAlgName)

    with open(destFilePath, 'w') as destFile:
        destFile.write(template)

## Focused on algorithms that support probabilistic predictions, multiclass and numerical + factor values. Some have been excluded because they don't work.

createScript("Classification", "mlr_c_template", "boosting", "default", "mfinal=100")
createScript("Classification", "mlr_c_template", "C50", "default", "subset = TRUE, bands = 0,  winnow = FALSE, noGlobalPruning = FALSE, CF = 0.25, minCases = 2, fuzzyThreshold = FALSE,  sample = 0, earlyStopping = TRUE")
createScript("Classification", "mlr_c_template", "ctree", "default", "eststat = c('quad', 'max'), testtype = c('Bonferroni', 'MonteCarlo', 'Univariate', 'Teststatistic'), mincriterion = 0.95, minsplit = 20, minbucket = 7, stump = FALSE, nresample = 9999, maxsurrogate = 0, mtry = 0, savesplitstats = TRUE, maxdepth = 0, remove_weights = FALSE")
createScript("Classification", "mlr_c_template", "gausspr", "default", "scaled = TRUE, type= NULL, kernel='rbfdot', kpar='automatic', var=1, variance.model = FALSE, tol=0.0005")
createScript("Classification", "mlr_c_template", "glmnet", "default", "fdev=1.0e-5, devmax=0.999, eps=1.0e-6, big=9.9e35, mnlam=5, pmin=1.0e-9, exmx=250.0,prec=1e-10,mxit=100,factory=FALSE")
createScript("Classification", "mlr_c_template", "h2o.deeplearning", "default", "balance_classes = FALSE, class_sampling_factors = NULL, max_after_balance_size = 5, max_hit_ratio_k = 0, checkpoint = NULL, pretrained_autoencoder = NULL, overwrite_with_best_model = TRUE, use_all_factor_levels = TRUE, standardize = TRUE, activation = c('Tanh', 'TanhWithDropout', 'Rectifier', 'RectifierWithDropout', 'Maxout', 'MaxoutWithDropout'), hidden = c(200, 200), epochs = 10, train_samples_per_iteration = -2, target_ratio_comm_to_comp = 0.05, seed = -1, adaptive_rate = TRUE, rho = 0.99, epsilon = 1e-08, rate = 0.005, rate_annealing = 1e-06, rate_decay = 1, momentum_start = 0, momentum_ramp = 1e+06, momentum_stable = 0, nesterov_accelerated_gradient = TRUE, input_dropout_ratio = 0, hidden_dropout_ratios = NULL, l1 = 0, l2 = 0, max_w2 = 3.4028235e+38, initial_weight_distribution = c('UniformAdaptive', 'Uniform', 'Normal'), initial_weight_scale = 1, initial_weights = NULL, initial_biases = NULL, loss = c('Automatic', 'CrossEntropy', 'Quadratic', 'Huber', 'Absolute', 'Quantile'), distribution = c('AUTO', 'bernoulli', 'multinomial', 'gaussian', 'poisson', 'gamma', 'tweedie', 'laplace', 'quantile', 'huber'), quantile_alpha = 0.5, tweedie_power = 1.5, huber_alpha = 0.9, score_interval = 5, score_training_samples = 10000, score_validation_samples = 0, score_duty_cycle = 0.1, classification_stop = 0, regression_stop = 1e-06, stopping_rounds = 5, stopping_metric = c('AUTO', 'deviance', 'logloss', 'MSE', 'RMSE', 'MAE', 'RMSLE', 'AUC', 'lift_top_group', 'misclassification', 'mean_per_class_error'), stopping_tolerance = 0, max_runtime_secs = 0, score_validation_sampling = c('Uniform', 'Stratified'), diagnostics = TRUE, fast_mode = TRUE, force_load_balance = TRUE, variable_importances = TRUE, replicate_training_data = TRUE, single_node_mode = FALSE, shuffle_training_data = FALSE, missing_values_handling = c('MeanImputation', 'Skip'), quiet_mode = FALSE, autoencoder = FALSE, sparse = FALSE, col_major = FALSE, average_activation = 0, sparsity_beta = 0, max_categorical_features = 2147483647, reproducible = FALSE, export_weights_and_biases = FALSE, mini_batch_size = 1, categorical_encoding = c('AUTO', 'Enum', 'OneHotInternal', 'OneHotExplicit', 'Binary', 'Eigen', 'LabelEncoder', 'SortByResponse', 'EnumLimited'), elastic_averaging = FALSE, elastic_averaging_moving_rate = 0.9, elastic_averaging_regularization = 0.001")
createScript("Classification", "mlr_c_template", "h2o.gbm", "default", "max_hit_ratio_k = 0, ntrees = 50, max_depth = 5, min_rows = 10, nbins = 20, nbins_top_level = 1024, nbins_cats = 1024, r2_stopping = Inf, stopping_rounds = 0, stopping_metric = c('AUTO', 'deviance', 'logloss', 'MSE', 'RMSE', 'MAE', 'RMSLE', 'AUC', 'lift_top_group', 'misclassification', 'mean_per_class_error'), stopping_tolerance = 0.001, max_runtime_secs = 0, seed = -1, build_tree_one_node = FALSE, learn_rate = 0.1, learn_rate_annealing = 1, distribution = c('AUTO', 'bernoulli', 'multinomial', 'gaussian', 'poisson', 'gamma', 'tweedie', 'laplace', 'quantile', 'huber'), quantile_alpha = 0.5, tweedie_power = 1.5, huber_alpha = 0.9, checkpoint = NULL, sample_rate = 1, sample_rate_per_class = NULL, col_sample_rate = 1, col_sample_rate_change_per_level = 1, col_sample_rate_per_tree = 1, min_split_improvement = 1e-05, histogram_type = c('AUTO', 'UniformAdaptive', 'Random', 'QuantilesGlobal', 'RoundRobin'), max_abs_leafnode_pred = Inf, pred_noise_bandwidth = 0, categorical_encoding = c('AUTO', 'Enum', 'OneHotInternal', 'OneHotExplicit', 'Binary', 'Eigen', 'LabelEncoder', 'SortByResponse', 'EnumLimited'), calibrate_model = FALSE, calibration_frame = NULL")
createScript("Classification", "mlr_c_template", "h2o.randomForest", "default", "max_hit_ratio_k = 0, ntrees = 50, max_depth = 20, min_rows = 1, nbins = 20, nbins_top_level = 1024, nbins_cats = 1024, r2_stopping = Inf, stopping_rounds = 0, stopping_metric = c('AUTO', 'deviance', 'logloss', 'MSE', 'RMSE', 'MAE', 'RMSLE', 'AUC', 'lift_top_group', 'misclassification', 'mean_per_class_error'), stopping_tolerance = 0.001, max_runtime_secs = 0, seed = -1, build_tree_one_node = FALSE, mtries = -1, sample_rate = 0.6320000291, sample_rate_per_class = NULL, binomial_double_trees = FALSE, checkpoint = NULL, col_sample_rate_change_per_level = 1, col_sample_rate_per_tree = 1, min_split_improvement = 1e-05, histogram_type = c('AUTO', 'UniformAdaptive', 'Random', 'QuantilesGlobal', 'RoundRobin'), categorical_encoding = c('AUTO', 'Enum', 'OneHotInternal', 'OneHotExplicit', 'Binary', 'Eigen', 'LabelEncoder', 'SortByResponse', 'EnumLimited'), calibrate_model = FALSE, calibration_frame = NULL")
createScript("Classification", "mlr_c_template", "ksvm", "default", "scaled = TRUE, type = NULL, kernel ='rbfdot', kpar = 'automatic', C = 1, nu = 0.2, epsilon = 0.1, prob.model = FALSE, class.weights = NULL, cross = 0, fit = TRUE, cache = 40, tol = 0.001, shrinking = TRUE")
createScript("Classification", "mlr_c_template", "kknn", "default", "k = 7, distance = 2, kernel = 'optimal', ykernel = NULL, scale=TRUE, contrasts = c('unordered' = 'contr.dummy', ordered = 'contr.ordinal')")
createScript("Classification", "mlr_c_template", "mlp", "default", "size = c(5), maxit = 100, initFunc = 'Randomize_Weights', initFuncParams = c(-0.3, 0.3), learnFunc = 'Std_Backpropagation', learnFuncParams = c(0.2, 0), updateFunc = 'Topological_Order', updateFuncParams = c(0), hiddenActFunc = 'Act_Logistic', shufflePatterns = TRUE, linOut = FALSE, outputActFunc = if (linOut) 'Act_Identity' else 'Act_Logistic'")
createScript("Classification", "mlr_c_template", "multinom", "default", "contrasts = NULL, Hess = FALSE, summ = 0, censored = FALSE")
createScript("Classification", "mlr_c_template", "naiveBayes", "default", "laplace = 0, threshold = 0.001, eps = 0")
createScript("Classification", "mlr_c_template", "randomForest", "default", "ntree=500, mtry=if (!is.null(y) && !is.factor(y)) max(floor(ncol(x)/3), 1) else floor(sqrt(ncol(x))), replace=TRUE, classwt=NULL, cutoff, strata, sampsize = if (replace) nrow(x) else ceiling(.632*nrow(x)), nodesize = if (!is.null(y) && !is.factor(y)) 5 else 1, maxnodes = NULL, importance=FALSE, localImp=FALSE, nPerm=1, proximity, oob.prox=proximity, norm.votes=TRUE, do.trace=FALSE, keep.forest=!is.null(y) && is.null(xtest), corr.bias=FALSE, keep.inbag=FALSE")
createScript("Classification", "mlr_c_template", "randomForestSRC", "default", "ntree = 1000, mtry = NULL, mtrySeq = NULL, nodesize = 5, nodesizeSeq = c(1:10,20,30,50,100), nsplit = 0, min.node = 3, use.org.features = TRUE, oob = TRUE")
createScript("Classification", "mlr_c_template", "ranger", "default", "num.trees = 500, mtry = NULL, importance = 'none', write.forest = TRUE, probability = FALSE, min.node.size = NULL, replace = TRUE, sample.fraction = ifelse(replace, 1, 0.632), case.weights = NULL, splitrule = NULL, num.random.splits = 1, alpha = 0.5, minprop = 0.1, split.select.weights = NULL, always.split.variables = NULL, respect.unordered.factors = NULL, scale.permutation.importance = FALSE, keep.inbag = FALSE, holdout = FALSE, num.threads = NULL, save.memory = FALSE, verbose = TRUE, seed = NULL, dependent.variable.name = NULL, status.variable.name = NULL, classification = NULL")
createScript("Classification", "mlr_c_template", "rda", "default", "gamma = NA,  lambda = NA, regularization = c(gamma = gamma, lambda = lambda),  crossval = TRUE, fold = 10, train.fraction = 0.5,  estimate.error = TRUE, output = FALSE, startsimplex = NULL,  max.iter = 100, trafo = TRUE, simAnn = FALSE, schedule = 2,  T.start = 0.1, halflife = 50, zero.temp = 0.01, alpha = 2,  K = 100")
createScript("Classification", "mlr_c_template", "rpart", "default", "method, parms, control, cost")
createScript("Classification", "mlr_c_template", "RRF", "default", "ntree=500, mtry=if (!is.null(y) && !is.factor(y)) max(floor(ncol(x)/3), 1) else floor(sqrt(ncol(x))), replace=TRUE, classwt=NULL, cutoff, strata, sampsize = if (replace) nrow(x) else ceiling(.632*nrow(x)), nodesize = if (!is.null(y) && !is.factor(y)) 5 else 1, maxnodes = NULL, importance=FALSE, localImp=FALSE, nPerm=1, proximity, oob.prox=proximity, norm.votes=TRUE, do.trace=FALSE, keep.forest=!is.null(y) && is.null(xtest), corr.bias=FALSE, keep.inbag=FALSE,  coefReg=NULL, flagReg=1, feaIni=NULL")
createScript("Classification", "mlr_c_template", "sda", "default", "lambda, lambda.var, lambda.freqs, diagonal=FALSE")
createScript("Classification", "mlr_c_template", "svm", "default", "scale = TRUE, type = NULL, kernel = 'radial', degree = 3, gamma = if (is.vector(x)) 1 else 1 / ncol(x), coef0 = 0, cost = 1, nu = 0.5, class.weights = NULL, cachesize = 40, tolerance = 0.001, epsilon = 0.1, shrinking = TRUE")
createScript("Classification", "mlr_c_template", "xgboost", "default", "nrounds, watchlist = list(), obj = NULL, feval = NULL, verbose = 1, print_every_n = 1L, early_stopping_rounds = NULL, maximize = NULL")

## Didn't work with default params: cforest nnet gbm mda qda lda
### Also didn't work: lda, saeDNN, nnTrain, dbnDNN, mda, xyf, extraTrees, sparseLDA, gbm

createScript("FeatureSelection", "mlr_f_template", "cforest.importance", "default", "")
createScript("FeatureSelection", "mlr_f_template", "kruskal.test", "default", "")
createScript("FeatureSelection", "mlr_f_template", "randomForestSRC.rfsrc", "default", "")
createScript("FeatureSelection", "mlr_f_template", "randomForestSRC.var.select", "default", "method = c('md', 'vh', 'vh.vimp'), conservative = c('medium', 'low', 'high'), ntree = (if (method == 'md') 1000 else 500), mvars = (if (method != 'md') ceiling(ncol(data)/5) else NULL), mtry = (if (method == 'md') ceiling(ncol(data)/3) else NULL), nodesize = 2, splitrule = NULL, nsplit = 10, xvar.wt = NULL, refit = (method != 'md'), fast = FALSE, always.use = NULL, nrep = 50, K = 5, nstep = 1")

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
