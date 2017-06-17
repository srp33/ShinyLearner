DESCRIPTION

    This command will execute each specified algorithm using a k-fold cross-validation strategy. It will perform classification and feature selection. It will use nested cross validation for algorithm selection and to select features and to optimize the number of selected features. It will output the predictive performance and selected features for each algorithm for the inner (nested) folds and will use a select-best method to make predictions for the outer folds.

REQUIRED ARGUMENTS

    --data [file_path]
    --description [description]
    --outer-iterations [number]
    --inner-iterations [number]
    --classif-algo [file_path]
    --fs-algo [file_path]
    --num-features [file_path]
    --output-dir [dir_path]

OPTIONAL ARGUMENTS

    --verbose [false|true]
    --temp-dir [dir_path]

EXAMPLE

    UserScripts/nestedboth_montecarlo
      --data Data.tsv.gz \
      --description "My_Interesting_Analysis" \
      --outer-iterations 10 \
      --inner-iterations 5 \
      --classif-algo "AlgorithmScripts/Classification/tsv/sklearn/svm_linear/default" \
      --fs-algo "AlgorithmScripts/FeatureSelection/tsv/sklearn/anova/default" \
      --num-features 5,10,50,100 \
      --output-dir Output/

NOTES

    The --data argument allows you to specify input data files in one of the supported formats (see https://github.com/srp33/ShinyLearner/blob/master/InputFormats.md).

    The --description value should be a user-friendly description of the analysis that will be performed. This description will be specified in the output files. If the description contains space characters, be sure to surround it in quotations.

    The --classif-algo argument allows you to specify classification algorithm(s) to be used in the analysis. The value should be a relative path to a script specified under AlgorithmScripts (see https://github.com/srp33/ShinyLearner/blob/master/Algorithms.md).

    The --fs-algo argument allows you to specify feature-selection algorithm(s) to be used in the analysis. The value(s) should be a relative path to a script specified under AlgorithmScripts (see https://github.com/srp33/ShinyLearner/blob/master/Algorithms.md).

    The --data, --classif-algo, and --fs-algo arguments must be used at least once but can be used multiple times. Wildcards may be used (in quotations).

    The --num-features argument should be used once. Multiple values should be separated by commas.

    The --outer-iterations and --inner-iterations values must be positive integers. These values indicate the number of times that cross-validation should be performed. The inner iterations are used for algorithm selection, while the outer iterations are used to assess generalizability of the selected models.

    The --output-dir argument allows you to indicate where output files will be stored. If this directory does not already exist, ShinyLearner will create it. For information about the output files that will be created, see https://github.com/srp33/ShinyLearner/blob/master/OutputFiles.md.

    If the --verbose argument is set to true, detailed information about the processing steps will be printed to standard out. This flag is typically used for debugging purposes.

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
