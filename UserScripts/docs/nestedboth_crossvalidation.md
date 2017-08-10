DESCRIPTION

    This command will execute each specified algorithm using a k-fold cross-validation strategy. It will perform classification and feature selection. It will use nested cross validation for algorithm selection and to select features and to optimize the number of selected features. It will output the predictive performance and selected features for each algorithm for the inner (nested) folds and will use a select-best method to make predictions for the outer folds.

REQUIRED ARGUMENTS

    --data [file_path]
    --description [description]
    --iterations [number]
    --outer-folds [number]
    --inner-folds [number]
    --classif-algo [file_path]
    --fs-algo [file_path]
    --num-features [file_path]
    --output-dir [dir_path]

OPTIONAL ARGUMENTS

    --verbose [false|true]
    --ohe [false|true]
    --scale [false|true]
    --impute [false|true]
    --temp-dir [dir_path]

EXAMPLE

    UserScripts/nestedboth_crossvalidation \
      --data Data.tsv.gz \
      --description "My_Interesting_Analysis" \
      --iterations 1 \
      --outer-folds 10 \
      --inner-folds 5 \
      --classif-algo "AlgorithmScripts/Classification/tsv/sklearn/svm_linear/default" \
      --fs-algo "AlgorithmScripts/FeatureSelection/tsv/sklearn/anova/default" \
      --num-features 5,10,50,100 \
      --scale true \
      --output-dir Output/

NOTES

    The --data argument allows you to specify input data files in one of the supported formats (see https://github.com/srp33/ShinyLearner/blob/master/InputFormats.md).

    The --description value should be a user-friendly description of the analysis that will be performed. This description will be specified in the output files. If the description contains space characters, be sure to surround it in quotations.

    The --classif-algo argument allows you to specify classification algorithm(s) to be used in the analysis. The value should be a relative path to a script specified under AlgorithmScripts (for example, AlgorithmScripts/Classification/tsv/sklearn/svm). Alternatively, you may specify the name of a text file that ends with ".list" and contains a list of algorithms (one per line) that you would like to include in the analysis. See https://github.com/srp33/ShinyLearner/blob/master/Algorithms.md for more information about algorithms. This argument may be specified multiple times. Wildcards may be used (in quotes).

    The --fs-algo argument allows you to specify feature-selection algorithm(s) to be used in the analysis. The value(s) should be a relative path to a script specified under AlgorithmScripts (for example, AlgorithmScripts/FeatureSelection/tsv/sklearn/anova). Alternatively, you may specify the name of a text file that ends with ".list" and contains a list of algorithms (one per line) that you would like to include in the analysis. See https://github.com/srp33/ShinyLearner/blob/master/Algorithms.md for more information about algorithms. This argument may be specified multiple times. Wildcards may be used (in quotes).

    The --data, --classif-algo, and --fs-algo arguments must be used at least once but can be used multiple times. Wildcards may be used (in quotations).

    The --num-features argument should be used once. Multiple values should be separated by commas.

    The --iterations value must be a positive integer. It indicates the number of times that a full round of cross-validation should be performed.

    The --outer-folds and --inner-folds arguments must be integers. If a value is 0 or is greater than or equal to the number of samples in the data set, leave-one-out cross validation will be used. If neither of these situations occurs, k-fold cross validation will be used, and the specified values will be used as k (a value of 1 is not allowed).

    The --output-dir argument allows you to indicate where output files will be stored. If this directory does not already exist, ShinyLearner will create it. For information about the output files that will be created, see https://github.com/srp33/ShinyLearner/blob/master/OutputFiles.md.

    The --verbose argument is set to false by default. If set to true, detailed information about the processing steps will be printed to standard out. This flag is typically used for debugging purposes.

    The --ohe argument is set to true by default. This means that any categorical variables will be [one-hot encoded](https://www.quora.com/What-is-one-hot-encoding-and-when-is-it-used-in-data-science).
    
    The --scale argument is set to false by default. When set to true, any continuous variable(s) will be scaled to zero mean and unit variance. Integers will be scaled only if more than 50% of values are unique.

    The --impute argument is set to false by default. When set to true, missing values will be imputed. Median-based imputation will be used for continuous and integer variables. Mode-based imputation will be used for discrete variables. Any variable missing more than 50% of values across all samples will be removed. Subsequently, any sample missing more than 50% of values across all features will be removed. In input data files, missing values should be specified as ?, NA, or null.
    
    When a value is specified for --temp-dir, temporary files will be stored in the specified location; otherwise, temporary files will be stored in the operating system's default location for temporary files.

OUTPUTS

    Metrics.tsv

    Predictions.tsv

    SelectedFeatures.tsv

    Nested_Metrics.tsv
    
    Nested_Predictions.tsv

    Nested_SelectedFeatures.tsv

    Nested_SelectedFeatures_Summarized.tsv
    
    Nested_Classification_ElapsedTime.tsv

    Nested_FeatureSelection_ElapsedTime.tsv

    Log.txt

    (Please see https://github.com/srp33/ShinyLearner/blob/master/OutputFiles.md for descriptions of what these files contain.)
