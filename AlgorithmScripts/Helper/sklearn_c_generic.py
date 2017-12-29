from pandas import read_csv
from numpy import array
from sys import argv
from sys import exit
from numpy import random

from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC

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
train_X = train_df.ix[:,:-1].values
train_y = array([classOptions.index(str(y[0])) for y in train_df.loc[:,["Class"]].values.tolist()])

test_X = readData(testFile).values

algorithmInstantiation = algorithmInstantiation.replace("{n_jobs}", numCores)

# Dynamically create the algorithm object
code = compile(algorithmInstantiation, "<string>", 'exec')
exec(code)

clf.fit(train_X, train_y)
print("Testing...3")
exit(1)
probs = clf.predict_proba(test_X)
#print("Testing...4")

for i in range(len(probs)):
    iProbs = list(probs[i])

    maxProb = max(iProbs)
    indicesMatchingMax = [i for i in range(len(iProbs)) if iProbs[i]==maxProb]
    random.shuffle(indicesMatchingMax)

    prediction = classOptions[indicesMatchingMax[0]]

    print("{}\t{}".format(prediction, "\t".join(["{:.9f}".format(iProb) for iProb in iProbs])))

#print("Testing...5")
#exit(0)
