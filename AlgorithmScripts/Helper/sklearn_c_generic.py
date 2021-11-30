#from sklearn.externals.joblib import parallel_backend

from numpy import array
from numpy import random
from pandas import read_csv
from sys import argv
from sys import exit

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import NuSVC
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

trainFile = argv[1]
testFile = argv[2]
classOptions = argv[3].split(",")
numCores = argv[4]
algorithmInstantiation = argv[5]

def readData(inFilePath):
    return read_csv(inFilePath, sep='\t', index_col=0)

R_SEED = 0
random.seed(R_SEED)

train_df = readData(trainFile)
train_X = train_df.iloc[:,:-1].values
train_y = array([classOptions.index(str(y[0])) for y in train_df.loc[:,["Class"]].values.tolist()])

test_X = readData(testFile).values

algorithmInstantiation = algorithmInstantiation.replace("{n_jobs}", numCores)
#print(algorithmInstantiation)
#exit(0)

# Dynamically create the algorithm object
code = compile(algorithmInstantiation, "<string>", 'exec')
exec(code)
#clf = ExtraTreesClassifier(n_estimators=1000, criterion='gini', max_depth=None, min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features=None, max_leaf_nodes=None, bootstrap=True, oob_score=False, class_weight=None, n_jobs=1, random_state=R_SEED, verbose=1, warm_start=False)

clf.fit(train_X, train_y)
probs = clf.predict_proba(test_X)

for i in range(len(probs)):
    iProbs = list(probs[i])

    maxProb = max(iProbs)
    indicesMatchingMax = [i for i in range(len(iProbs)) if iProbs[i]==maxProb]
    random.shuffle(indicesMatchingMax)

    prediction = classOptions[indicesMatchingMax[0]]

    print("{}\t{}".format(prediction, "\t".join(["{:.9f}".format(iProb) for iProb in iProbs])))

exit(0)
