## DESCRIPTION

The `nestedboth_montecarlo` command uses Monte Carlo cross-validation. It performs classification and can perform hyperparameter optimization as well as feature selection. It uses nested, Monte Carlo cross validation for hyperparameter optimization and feature selection. It outputs the performance of each algorithm for the inner (nested) folds and uses a select-best method for predictions in the outer folds. It also outputs a ranked list of features for each feature-selection algorithm as well as a Borda Count list of features based on the rankings of all feature-selection algorithms.

## REQUIRED ARGUMENTS

    --data [file_path]
    --description [description]
    --outer-iterations [integer]
    --inner-iterations [integer]
    --classif-algo [file_path]
    --fs-algo [file_path]
    --num-features [comma_separated_list]

The `--data` argument allows you to specify input data file(s) in one of the [supported formats](https://github.com/srp33/ShinyLearner/blob/master/InputFormats.md).

The `--description` value should be a user-friendly description of the analysis that will be performed. This description will be specified in the output files. If the description contains space characters, be sure to surround it in quotation marks.

The `--outer-iterations` value must be a positive integer. This value indicates the number of times that cross-validation should be performed on the outer folds.

The `--inner-iterations` value must be a positive integer. The inner iterations are used for hyperparameter optimization, while the outer iterations are used to assess generalizability of the selected parameters. This value indicates the number of times that cross-validation should be performed. 

The `--classif-algo` argument allows you to specify a classification algorithm to be used in the analysis. The value should be a relative path to a script specified under the AlgorithmScripts directory (for example, `AlgorithmScripts/Classification/tsv/sklearn/svm`). The paths may contain wildcard characters (surround the path in quotes). Alternatively, you may specify the name of a text file that ends with ".list" and contains a list of [algorithms](https://github.com/srp33/ShinyLearner/blob/master/Algorithms.md) (one per line).

The `--fs-algo` argument allows you to specify [feature-selection algorithm(s)](https://github.com/srp33/ShinyLearner/blob/master/Algorithms.md) to be used in the analysis. The value should be a relative path to a script specified under AlgorithmScripts (for example, `AlgorithmScripts/FeatureSelection/tsv/sklearn/anova`). Alternatively, you may specify the name of a text file that ends with ".list" and contains a list of algorithms (one per line).

The `--num-features` argument indicates the number of top-ranked features that should be used in nested cross-validation in an attempt to identify the optimal number of features for classification. Multiple values should be separated by commas.

The `--data`, `--classif-algo`, and `--fs-algo` arguments must be used at least once but can be used multiple times. Wildcards may be used (in quotations).

## OPTIONAL ARGUMENTS

    --verbose [false|true]
    --seed [integer]
    --train-proportion [float]
    --ohe [false|true]
    --scale [none|standard|robust|minmax|maxabs|power|quantnorm|quantunif|normalizer]
    --impute [false|true]
    --num-cores [integer]
    --temp-dir [dir_path]

The `--verbose` argument is set to `false` by default. If set to `true`, detailed information about the processing steps will be printed to standard out. This flag is typically used for debugging purposes.

The `--seed` argument allows the user to specify a random seed for assigning samples to training and test set(s). This value is `1` by default.

The `--train-proportion` argument allows the user to control the proportion of samples that are assigned (randomly) to each training set. The remaining samples are assigned to the corresponding test sets. By default, this value is `0.67`. Valid values range between `0.1` and `0.9`.

The `--ohe` argument is set to `true` by default. If set to `true`, any categorical variable in the data will be [one-hot encoded](https://www.quora.com/What-is-one-hot-encoding-and-when-is-it-used-in-data-science).

The `--scale` argument is set to `none` by default (no scaling is performed). When set to one of the other options, any continuous variable will be scaled using the specified method. Information about the scaling methods can be found on the [scikit-learn site](https://scikit-learn.org/stable/auto_examples/preprocessing/plot_all_scaling.html#sphx-glr-auto-examples-preprocessing-plot-all-scaling-py). Continuous variables will be scaled only if *more than* 50% of values are unique.

The `--impute` argument is set to `false` by default. When set to `true`, missing values will be imputed. In input data files, missing values should be specified as ?, NA, or null. Median-based imputation will be used for continuous and integer variables. Mode-based imputation will be used for discrete variables. Any variable missing more than 50% of values across all samples will be removed. Subsequently, any sample missing more than 50% of values across all features will be removed.

The `--num-cores` argument is set to `1` by default. When set to a number greater than `1`, ShinyLearner will attempt to use multiple cores when executing a given algorithm. Not every algorithm supports multi-core processing.

When a value is specified for `--temp-dir`, temporary files will be stored in the specified location; otherwise, temporary files will be stored in the operating system's default location for temporary files.

## OUTPUT FILES

Please go [here](https://github.com/srp33/ShinyLearner/blob/master/OutputFiles.md) for descriptions of what these output files contain.

* Metrics.tsv

* Predictions.tsv

* SelectedFeatures.tsv

* Nested_Metrics.tsv

* Nested_Predictions.tsv

* Nested_SelectedFeatures.tsv

* Nested_SelectedFeatures_Summarized.tsv

* Nested_Classification_ElapsedTime.tsv

* Nested_FeatureSelection_ElapsedTime.tsv

* Log.txt

## EXAMPLE

The following example illustrates how to execute ShinyLearner using [Docker](https://www.docker.com) on a Unix-based system (e.g., Linux or Mac OS). For additional help or to learn about executing the software on Windows, go [here](http://bioapps.byu.edu/shinylearner/).

The first command creates the output directory if it doesn't already exist.

The second (long) command executes ShinyLearner within a Docker container. 

* The `-v` arguments tell Docker where to find and store files on your computer. In the example below, the first `-v` argument specifies the directory where the input data files are stored on your computer. In this example, the data files would be stored in the current working directory (`$(pwd)`). The path *after* the colon indicates the path that ShinyLearner will use to access these files within the container (`/InputData`.) If your data files are stored in a location other than the current working directory, you could use something like this: `-v /some/other/directory:/InputData`. It must be an *absolute* path (the `~` shortcut is not supported).

* The second `-v` argument specifies the directory where the output files will be placed after ShinyLearner performs the analysis. In the example below, the output files would be stored in a directory called `Output` that is a subdirectory of the current working directory (`$(pwd)`). (Within the Docker container, ShinyLearner will access these files via `/OutputData`.) If you want the output files to be placed somewhere else, you could use something like this: `-v /some/other/directory:/OutputData`. It must be an *absolute* path (the `~` shortcut is not supported).

The fourth line in the Docker command tells Docker to run under the current user's account.

The fifth line in the Docker command indicates the name and version of the Docker image to be used.

Some algorithms support the use of graphical processing units for faster performance. To use this, you must install [nvidia-docker](https://github.com/NVIDIA/nvidia-docker) and substitute `srp33/shinylearner` with `srp33/shinylearner_gpu` in the Docker command that you execute.

    mkdir -p $(pwd)/Output

    docker run --rm -i \
      -v "$(pwd)"/:"/InputData" \
      -v "$(pwd)/Output":"/OutputData" \
      --user $(id -u):$(id -g) \
      srp33/shinylearner:version594 \
      UserScripts/nestedboth_montecarlo \
        --data Data.tsv.gz \
        --description "My_Interesting_Analysis" \
        --outer-iterations 10 \
        --inner-iteration 5 \
        --classif-algo "AlgorithmScripts/Classification/tsv/sklearn/svm/default*" \
        --fs-algo "AlgorithmScripts/FeatureSelection/tsv/sklearn/anova/default" \
        --seed 1 \
        --num-features 5,10,50,100 \
        --scale robust
