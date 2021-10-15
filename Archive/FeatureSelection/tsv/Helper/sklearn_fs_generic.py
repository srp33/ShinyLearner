from sys import argv
from pandas import read_csv
from numpy import float32
from numpy import array
from numpy import lexsort
from numpy import random

trainFilePath = argv[1]
algorithm = argv[2]

def readData(inFilePath):
    return read_csv(inFilePath, sep='\t', index_col=0)

def rank_features(algorithm, X, y):
    # The RFE approach can be used with various different classifiers
    if algorithm == 'random_forest_rfe':
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.feature_selection import RFE
        estimator = RandomForestClassifier(n_estimators=50, random_state=R_SEED, n_jobs=1)
        selector = RFE(estimator, 5, step=0.1)
        selector.fit(X, y)

        for x in sorted(zip(map(lambda x: round(x, 4), selector.ranking_), features)):
            print x[1]
    elif algorithm == 'svm_rfe':
        from sklearn.svm import SVC
        from sklearn.feature_selection import RFE
        estimator = SVC(random_state=R_SEED, kernel='linear')
        selector = RFE(estimator, 5, step=0.1)
        selector.fit(X, y)

        for x in sorted(zip(map(lambda x: round(x, 4), selector.ranking_), features)):
            print x[1]
    elif algorithm == 'random_logistic_regression':
        # See http://blog.datadive.net/selecting-good-features-part-iv-stability-selection-rfe-and-everything-side-by-side/
        from sklearn.linear_model import RandomizedLogisticRegression
        rlasso = RandomizedLogisticRegression(random_state=R_SEED)
        rlasso.fit(X, y)

        for x in sorted(zip(map(lambda x: round(x, 4), rlasso.scores_), features), reverse=True):
            print x[1]
    elif algorithm == 'random_lasso':
        from sklearn.linear_model import RandomizedLasso
        rlasso = RandomizedLasso(random_state=R_SEED)
        #rlasso = RandomizedLasso(alpha=0.025, random_state=R_SEED)
        rlasso.fit(X, y)

        for x in sorted(zip(map(lambda x: round(x, 4), rlasso.scores_), features), reverse=True):
            print x[1]
    elif algorithm == 'anova':
        from sklearn.feature_selection import f_classif
        F, pval = f_classif(X, y)
        random_array = random.random(len(pval))
        order = lexsort((random_array,pval)) # will break ties by random
        for i in order:
            print features[i]
    else:
        print "Invalid algorithm: %s" % algorithm
        exit(1)

R_SEED = 0
random.seed(R_SEED)

train_df = readData(trainFilePath)
train_X = train_df.ix[:,:-1].values

train_y = [y[0] for y in train_df.loc[:,["Class"]].values.tolist()]
classOptions = sorted(list(set(train_y)))
train_y = array([classOptions.index(y) for y in train_y])

features = list(train_df.columns.values)[:-1]
rank_features(algorithm, train_X, train_y)
