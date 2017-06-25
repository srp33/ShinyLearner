# See http://blog.datadive.net/selecting-good-features-part-iv-stability-selection-rfe-and-everything-side-by-side/

from sys import argv
from pandas import read_csv
from numpy import float32
from numpy import array
from numpy import lexsort
from numpy import random

dataFilePath = argv[1]
algorithmClass = argv[2]
algorithmInstantiation = argv[3]

R_SEED = 0
random.seed(R_SEED)

train_df = read_csv(dataFilePath, sep='\t', index_col=0)
train_X = train_df.ix[:,:-1].values

train_y = [y[0] for y in train_df.loc[:,["Class"]].values.tolist()]
classOptions = sorted(list(set(train_y)))
train_y = array([classOptions.index(y) for y in train_y])

features = list(train_df.columns.values)[:-1]

# Dynamically execute code
code = compile(algorithmInstantiation, "<string>", 'exec')
exec code

rankedFeatures = None

if algorithmClass == 'score':
    random_array = random.random(len(score))
    order = lexsort((random_array, score)) # will break ties by random

    rankedFeatures = [features[i] for i in order]

# The RFE approach can be used with various different classifiers
elif algorithmClass == 'rfe':
    selector = RFE(estimator, n_features_to_select=5, step=0.1)
    selector.fit(train_X, train_y)

    rankedFeatures = [y[1] for y in sorted(zip(map(lambda x: round(x, 4), selector.ranking_), features))]

elif algorithmClass == 'coef':
    scorer.fit(train_X, train_y)
    rankedFeatures = [y[1] for y in sorted(zip(map(lambda x: round(x, 4), scorer.scores_), features), reverse=True)]

else:
    print("Invalid algorithm type.")

print ",".join(rankedFeatures)
