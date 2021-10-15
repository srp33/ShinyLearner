from pandas import read_csv
from numpy import array
from sys import argv
from sys import exit
from numpy import random

trainFile = argv[1]
testFile = argv[2]
classOptions = argv[3].split(",")
algorithm = argv[4]

def readData(inFilePath):
    return read_csv(inFilePath, sep='\t', index_col=0)

def predict(algorithm, train_X, train_y, test_X):
    if algorithm == 'lda':
        from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
        clf = LinearDiscriminantAnalysis()
    elif algorithm == 'qda':
        from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
        clf = QuadraticDiscriminantAnalysis()
    elif algorithm == 'random_forest':
        from sklearn.ensemble import RandomForestClassifier
        clf = RandomForestClassifier(n_estimators=100, random_state=R_SEED)
    elif algorithm == 'bagging':
        from sklearn.ensemble import BaggingClassifier
        clf = BaggingClassifier(n_estimators=100, random_state=R_SEED)
    elif algorithm == 'extra_trees':
        from sklearn.ensemble import ExtraTreesClassifier
        clf = ExtraTreesClassifier(n_estimators=100, random_state=R_SEED)
    elif algorithm == 'logistic_regression':
        from sklearn.linear_model import LogisticRegression
        clf = LogisticRegression(random_state=R_SEED)
#    elif algorithm == 'passive_aggressive':
#        from sklearn.linear_model import PassiveAggressiveClassifier
#        clf = PassiveAggressiveClassifier(random_state=R_SEED)
#    elif algorithm == 'elastic_net':
#        from sklearn.linear_model import ElasticNet
#        clf = ElasticNet(random_state=R_SEED)
#    elif algorithm == 'ridge':
#        from sklearn.linear_model import RidgeClassifier
#        clf = RidgeClassifier(random_state=R_SEED)
    elif algorithm == 'sgd':
        from sklearn.linear_model import SGDClassifier
        clf = SGDClassifier(random_state=R_SEED, loss="modified_huber")
    elif algorithm == 'knn':
        from sklearn.neighbors import KNeighborsClassifier
        clf = KNeighborsClassifier()
#    elif algorithm == 'radius_neighbors':
#        from sklearn.neighbors import RadiusNeighborsClassifier
#        clf = RadiusNeighborsClassifier()
    #elif algorithm == 'nearest_centroid':
    #    from sklearn.neighbors.nearest_centroid import NearestCentroid
    #    clf = NearestCentroid()
    #elif algorithm == 'bernoulli_rbm':
    #    from sklearn.neural_network import BernoulliRBM
    #    clf = BernoulliRBM(random_state=R_SEED)
    elif algorithm == 'svm_linear':
        from sklearn.svm import SVC
        clf = SVC(probability=True, random_state=R_SEED, kernel='linear')
    elif algorithm == 'svm_rbf':
        from sklearn.svm import SVC
        clf = SVC(probability=True, random_state=R_SEED, kernel='rbf')
    elif algorithm == 'svm_poly':
        from sklearn.svm import SVC
        clf = SVC(probability=True, random_state=R_SEED, kernel='poly')
    elif algorithm == 'svm_sigmoid':
        from sklearn.svm import SVC
        clf = SVC(probability=True, random_state=R_SEED, kernel='sigmoid')
    elif algorithm == 'svm_nurbf':
        from sklearn.svm import NuSVC
        clf = NuSVC(probability=True, random_state=R_SEED)
    elif algorithm == 'decision_tree':
        from sklearn.tree import DecisionTreeClassifier
        clf = DecisionTreeClassifier(random_state=R_SEED)
    else:
        print "Invalid algorithm: %s" % algorithm
        exit(1)

    clf.fit(train_X, train_y)
    return clf.predict_proba(test_X)

R_SEED = 0
random.seed(R_SEED)

train_df = readData(trainFile)
train_X = train_df.ix[:,:-1].values
train_y = array([classOptions.index(str(y[0])) for y in train_df.loc[:,["Class"]].values.tolist()])

test_X = readData(testFile).values

probs = predict(algorithm, train_X, train_y, test_X)

for i in range(len(probs)):
    iProbs = list(probs[i])

    maxProb = max(iProbs)
    indicesMatchingMax = [i for i in range(len(iProbs)) if iProbs[i]==maxProb]
    random.shuffle(indicesMatchingMax)

    prediction = classOptions[indicesMatchingMax[0]]

    print "%s\t%s" % (prediction, "\t".join(["%.9f" % iProb for iProb in iProbs]))
