DESCRIPTION

    This command will execute each specified algorithm using a Monte Carlo cross-validation strategy. It will perform classification but not feature selection or algorithm optimization. It will output the performance of each algorithm and will use a majority-vote method to make multiple-classifier predictions.

REQUIRED ARGUMENTS

    --data [file_path]
    --description [description]
    --iterations [integer]
    --classif-algo [file_path]
    --output-dir [dir_path]

OPTIONAL ARGUMENTS

    --verbose [false|true]
    --seed [integer]
    --ohe [false|true]
    --temp-dir [dir_path]

EXAMPLE

    UserScripts/classification_montecarlo \
      --data Data.tsv.gz \
      --description "My_Interesting_Analysis" \
      --iterations 10 \
      --classif-algo "AlgorithmScripts/Classification/tsv/sklearn/svm_linear/default" \
      --output-dir Output/ \
      --seed 33

NOTES

    The --data argument allows you to specify input data files in one of the supported formats (see https://github.com/srp33/ShinyLearner/blob/master/InputFormats.md).

    The --description value should be a user-friendly description of the analysis that will be performed. This description will be specified in the output files. If the description contains space characters, be sure to surround it in quotations.

    The --classif-algo argument allows you to specify classification algorithm(s) to be used in the analysis. The value should be a relative path to a script specified under AlgorithmScripts (see https://github.com/srp33/ShinyLearner/blob/master/Algorithms.md).

    The --data and --classif-algo arguments must be used at least once but can be used multiple times. Wildcards may be used (in quotations).

    The --iterations value must be a positive integer. It indicates the number of times that a round of cross-validation should be performed.

    The --output-dir argument allows you to indicate where output files will be stored. If this directory does not already exist, ShinyLearner will create it. For information about the output files that will be created, see https://github.com/srp33/ShinyLearner/blob/master/OutputFiles.md.

    The --verbose argument is set to false by default. If set to true, detailed information about the processing steps will be printed to standard out. This flag is typically used for debugging purposes.

    The --seed argument allows the user to specify a random seed for assigning samples to training and test set(s). This value is 1 by default.

    The --ohe argument is set to true by default. This means that any categorical variables will be [one-hot encoded](https://www.quora.com/What-is-one-hot-encoding-and-when-is-it-used-in-data-science).
    
    When a value is specified for --temp-dir, temporary files will be stored in the specified location; otherwise, temporary files will be stored in the operating system's default location for temporary files.

OUTPUTS

    Metrics.tsv

    Predictions.tsv

    ElapsedTime.tsv

    Log.txt

    (Please see https://github.com/srp33/ShinyLearner/blob/master/OutputFiles.md for descriptions of what these files contain.)
