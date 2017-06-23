from sys import argv
from pandas import read_csv
from numpy import float32
from numpy import array
from numpy import lexsort
from numpy import random

trainFilePath = argv[1]
algorithm = argv[2]
parameterDescription = argv[3]

def rank_features(algorithm, X, y):
    if algorithm == 'anova':
        from sklearn.feature_selection import f_classif
        F, pval = f_classif(X, y)
        random_array = random.random(len(pval))
        order = lexsort((random_array,pval)) # will break ties by random

        return [features[i] for i in order]

    elif algorithm == 'mutual_info':
        from sklearn.feature_selection import mutual_info_classif
        scorer = mutual_info_classif(random_state=R_SEED)
        scorer.fit(X, y)

        return [y[1] for y in sorted(zip(map(lambda x: round(x, 4), scorer.scores_), features))]

    # The RFE approach can be used with various different classifiers
    elif algorithm == 'random_forest_rfe':
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.feature_selection import RFE
        ####estimator = RandomForestClassifier(n_estimators=50, random_state=R_SEED, n_jobs=1)
        estimator = RandomForestClassifier(random_state=R_SEED)
        selector = RFE(estimator, n_features_to_select=5, step=0.1)
        selector.fit(X, y)

        return [y[1] for y in sorted(zip(map(lambda x: round(x, 4), selector.ranking_), features))]
    elif algorithm == 'random_lasso':
        from sklearn.linear_model import RandomizedLasso
        scorer = RandomizedLasso(random_state=R_SEED)
        scorer.fit(X, y)

        #return [y[1] for y in sorted(zip(map(lambda x: round(x, 4), scorer.scores_), features), reverse=True)]
        return [y[1] for y in sorted(zip(map(lambda x: round(x, 4), scorer.scores_), features))]

    elif algorithm == 'random_logistic_regression':
        # See http://blog.datadive.net/selecting-good-features-part-iv-stability-selection-rfe-and-everything-side-by-side/
        from sklearn.linear_model import RandomizedLogisticRegression
        scorer = RandomizedLogisticRegression(random_state=R_SEED)
        scorer.fit(X, y)

        return [y[1] for y in sorted(zip(map(lambda x: round(x, 4), scorer.scores_), features), reverse=True)]

    elif algorithm == 'svm_rfe':
        from sklearn.svm import SVC
        from sklearn.feature_selection import RFE
        estimator = SVC(random_state=R_SEED, kernel='linear')
        selector = RFE(estimator, n_features_to_select=5, step=0.1)
        selector.fit(X, y)

        return [y[1] for y in sorted(zip(map(lambda x: round(x, 4), selector.ranking_), features))]

    else:
        print "Invalid algorithm: %s" % algorithm
        exit(1)

R_SEED = 0
random.seed(R_SEED)

train_df = read_csv(trainFilePath, sep='\t', index_col=0)
train_X = train_df.ix[:,:-1].values

train_y = [y[0] for y in train_df.loc[:,["Class"]].values.tolist()]
classOptions = sorted(list(set(train_y)))
train_y = array([classOptions.index(y) for y in train_y])

features = list(train_df.columns.values)[:-1]

print ",".join(rank_features(algorithm, train_X, train_y))
