DESCRIPTION

    This command will execute each specified algorithm using a k-fold cross-validation strategy. It will perform classification and feature selection. It will use nested cross validation for algorithm selection and to select features and to optimize the number of selected features. It will output the predictive performance and selected features for each algorithm for the inner (nested) folds and will use a select-best method to make predictions for the outer folds.

REQUIRED ARGUMENTS

    --data [file_path]
    --description [description]
    --outer-iterations [integer]
    --inner-iterations [integer]
    --classif-algo [file_path]
    --fs-algo [file_path]
    --num-features [comma_separated_list]
    --output-dir [dir_path]

OPTIONAL ARGUMENTS

    --verbose [false|true]
    --seed [integer]
    --train-proportion [float]
    --ohe [false|true]
    --scale [none|standard|robust|minmax|maxabs|power|quantnorm|quantunif|normalizer]
    --impute [false|true]
    --num-cores [integer]
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
      --seed 33 \
      --scale robust \
      --output-dir Output/

NOTES

    The --data argument allows you to specify input data files in one of the supported formats (see https://github.com/srp33/ShinyLearner/blob/master/InputFormats.md).

    The --description value should be a user-friendly description of the analysis that will be performed. This description will be specified in the output files. If the description contains space characters, be sure to surround it in quotations.

    The --classif-algo argument allows you to specify classification algorithm(s) to be used in the analysis. The value should be a relative path to a script specified under AlgorithmScripts (for example, AlgorithmScripts/Classification/tsv/sklearn/svm). Alternatively, you may specify the name of a text file that ends with ".list" and contains a list of algorithms (one per line) that you would like to include in the analysis. See https://github.com/srp33/ShinyLearner/blob/master/Algorithms.md for more information about algorithms. This argument may be specified multiple times. Wildcards may be used (in quotes).

    The --fs-algo argument allows you to specify feature-selection algorithm(s) to be used in the analysis. The value(s) should be a relative path to a script specified under AlgorithmScripts (for example, AlgorithmScripts/FeatureSelection/tsv/sklearn/anova). Alternatively, you may specify the name of a text file that ends with ".list" and contains a list of algorithms (one per line) that you would like to include in the analysis. See https://github.com/srp33/ShinyLearner/blob/master/Algorithms.md for more information about algorithms. This argument may be specified multiple times. Wildcards may be used (in quotes).

    The --data, --classif-algo, and --fs-algo arguments must be used at least once but can be used multiple times. Wildcards may be used (in quotations).

    The --num-features argument should be used once. It indicates the number of top-ranked features that should be used in nested cross-validation in an attempt to identify the optimal number of features to use for classification. Multiple values should be separated by commas.

    The --outer-iterations and --inner-iterations values must be positive integers. These values indicate the number of times that cross-validation should be performed. The inner iterations are used for algorithm selection, while the outer iterations are used to assess generalizability of the selected models.

    The --output-dir argument allows you to indicate where output files will be stored. If this directory does not already exist, ShinyLearner will create it. For information about the output files that will be created, see https://github.com/srp33/ShinyLearner/blob/master/OutputFiles.md.

    The --verbose argument is set to false by default. If set to true, detailed information about the processing steps will be printed to standard out. This flag is typically used for debugging purposes.

    The --seed argument allows the user to specify a random seed for assigning samples to training and test set(s). This value is 1 by default.

    The --train-proportion argument allows the user to control the proportion of samples that are assigned (randomly) to each training set. The remaining samples are assigned to the corresponding test sets. By default, this value is 0.67. Valid values range between 0.1 and 0.9.

    The --ohe argument is set to true by default. This means that any categorical variables will be [one-hot encoded](https://www.quora.com/What-is-one-hot-encoding-and-when-is-it-used-in-data-science).
    
    The --scale argument is set to none by default (no scaling is performed). When set to one of the other options, any continuous variable(s) will be scaled using the specified method. Information about the scaling methods can be found on the [scikit-learn site](https://scikit-learn.org/stable/auto_examples/preprocessing/plot_all_scaling.html#sphx-glr-auto-examples-preprocessing-plot-all-scaling-py). Continuous variables will be scaled only if more than 50% of values are unique.

    The --impute argument is set to false by default. When set to true, missing values will be imputed. Median-based imputation will be used for continuous and integer variables. Mode-based imputation will be used for discrete variables. Any variable missing more than 50% of values across all samples will be removed. Subsequently, any sample missing more than 50% of values across all features will be removed. In input data files, missing values should be specified as ?, NA, or null.

    The --num-cores argument is set to 1 by default. When set to a number greater than 1, it will attempt to use multiple cores when executing a given algorithm. Not every algorithm supports parallelization.
    
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
