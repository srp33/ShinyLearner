from sys import argv
from pandas import read_csv

# Parse command-line arguments
trainFilePath = argv[1]
testFilePath = argv[2]
classOptions = argv[3].split(",")
numCores = argv[4]
algorithmInstantiation = argv[5]
verbose = argv[6] == "true"
arg1 = int(argv[7])
arg2 = argv[8] == "true"

# Set a random seed (assuming there is a stochastic nature to your algorithm)
random.seed(0)

# Use pandas to read the training file path
train_df = read_csv(trainFilePath, sep='\t', index_col=0)

# Parse the predictor variables from the training data, ignoring the class variable
train_X = train_df.ix[:,:-1].values

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
