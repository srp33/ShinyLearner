from sys import argv
from pandas import read_csv
from numpy import random
from numpy import array

# Parse command-line arguments
trainFilePath = argv[1]
testFilePath = argv[2]
classOptions = argv[3].split(",")
numCores = argv[4]
verbose = argv[5] == "true"
arg1 = int(argv[6])
arg2 = argv[7] == "true"

# Set a random seed (assuming there is a stochastic nature to your algorithm)
random.seed(0)

# Use pandas to read the training file path
train_df = read_csv(trainFilePath, sep='\t', index_col=0)

# Parse the predictor variables from the training data, ignoring the class variable
train_X = train_df.iloc[:,:-1].values

# Parse the class labels from the training data
# Convert these labels to integers in the order specified by classOptions
train_y = array([classOptions.index(str(y[0])) for y in train_df.loc[:,["Class"]].values.tolist()])

# Use pandas to read the test file path
test_X = read_csv(testFilePath, sep='\t', index_col=0).values

###########################################
#
# Fit the model (use arg1, arg2, arg3)...
#
# Make predictions...
#
# Print the predictions for each test instance to standard out...
#   The predictions must be printed in the same order that they were listed in the test file.
#   For each test instance, please print the following (separated by tabs):
#     1. Predicted class
#     2. Probabilistic prediction for the first class option
#     3. Probabilistic prediction for the second class option
#     4. Probabilistic prediction for additional class options (if more than two classes)
#
###########################################

for testSample in test_X: # In real life, we wouldn't do this...
    fakeProbabilities = ["0.0" for x in classOptions] # In real life, the probabilities would sum to 1.0
    print("{}\t{}".format(classOptions[0], "\t".join(fakeProbabilities)))
