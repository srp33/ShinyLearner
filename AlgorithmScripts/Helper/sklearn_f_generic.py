# See http://blog.datadive.net/selecting-good-features-part-iv-stability-selection-rfe-and-everything-side-by-side/

from sys import argv
from pandas import read_csv
from numpy import float32
from numpy import array
from numpy import lexsort
from numpy import random

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import f_classif
from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_selection import RFE
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.svm import SVC

dataFilePath = argv[1]
numCores = argv[2]
algorithmClass = argv[3]
algorithmInstantiation = argv[4]

algorithmInstantiation = algorithmInstantiation.replace("{n_jobs}", numCores)

R_SEED = 0
random.seed(R_SEED)

train_df = read_csv(dataFilePath, sep='\t', index_col=0)
train_X = train_df.iloc[:,:-1].values

train_y = [y[0] for y in train_df.loc[:,["Class"]].values.tolist()]
classOptions = sorted(list(set(train_y)))
train_y = array([classOptions.index(y) for y in train_y])

features = list(train_df.columns.values)[:-1]

# Dynamically execute code
code = compile(algorithmInstantiation, "<string>", 'exec')
exec(code)

rankedFeatures = None

if algorithmClass == 'score':
    random_array = random.random(len(score))
    order = lexsort((random_array, score)) # will break ties by random

    rankedFeatures = [features[i] for i in order]

# The RFE approach can be used with various different classifiers
elif algorithmClass == 'rfe':
    selector.fit(train_X, train_y)

    rankedFeatures = [y[1] for y in sorted(zip(map(lambda x: round(x, 4), selector.ranking_), features))]

#Not used?
elif algorithmClass == 'coef':
    scorer.fit(train_X, train_y)
    rankedFeatures = [y[1] for y in sorted(zip(map(lambda x: round(x, 4), scorer.scores_), features), reverse=True)]

# This currently doesn't work but could be added in the future.
# It only returns the list of selected features.
# It doesn't return a ranking. I believe ShinyLearner would need to be modified to work with this.
#elif algorithmClass == 'wrapper':
#    wrapper.fit(train_X, train_y)
#    rankedFeatures = features[wrapper.get_support()]
else:
    print("Invalid algorithm type.")

print(",".join(rankedFeatures))
