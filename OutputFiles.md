# Output Files

ShinyLearner produces output files that follow the [tidy data](http://vita.had.co.nz/papers/tidy-data.pdf) principles. This affords extra flexibility and consistency when interpreting the results. These tab-delimited text files can be imported directly into third-party analytic tools, such as Microsoft Excel, R, or Python. The descriptions below indicate what each output file contains. The [UserScripts documentation](https://github.com/srp33/ShinyLearner/tree/master/UserScripts/docs) indicates which output files are produced for each type of analysis.

## Metrics.tsv

* Indicates [classification measures](https://github.com/srp33/ShinyLearner/blob/master/Metrics.md).
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/Metrics.tsv)

## Predictions.tsv

* Contains individual-level predictions for each sample/instance for which predictions were made.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/Predictions.tsv)

## SelectedFeatures.tsv

* A ranked list of features for each feature-selection algorithm.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/SelectedFeatures.tsv)
* Note: If multiple data files were used as input, the path to the file name will be used as a prefix before each feature name.

## ElapsedTime.tsv

* Indicates how long it took for each algorithm to execute.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/ElapsedTime.tsv)

When nested cross validation is used to optimize hyperparameters or to select features, ShinyLearner produces output files that describe algorithm performance within the training sets. The following descriptions indicate what these files contain.

## Nested_Metrics.tsv

* Indicates [classification measures](https://github.com/srp33/ShinyLearner/blob/master/Metrics.md) for the nested training/test sets.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/Nested_Metrics.tsv)

## Nested_Best.tsv

* Indicates which hyperparameter combination performed best for each classification algorithm.

## Nested_Predictions.tsv

* Contains individual-level predictions for each sample/instance for which predictions were made for each algorithm.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/Nested_Predictions.tsv)

## Nested_SelectedFeatures.tsv

* A ranked list of features for each feature-selection algorithm.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/Nested_SelectedFeatures.tsv)
* Note: If multiple data files were used as input, the path to the file name will be used as a prefix before each feature name.

## Nested_SelectedFeatures_Summarized.tsv

* A ranked list of features, averaged (using [Borda count](https://en.wikipedia.org/wiki/Borda_count)) across all iterations, for each feature-selection algorithm.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/Nested_SelectedFeatures_Summarized.tsv)
* Note: If multiple data files were used as input, the path to the file name will be used as a prefix before each feature name.

## Nested_Classification_ElapsedTime.tsv

* Indicates how long it took for each classification algorithm to execute.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/Nested_Classification_ElapsedTime.tsv)

## Nested_FeatureSelection_ElapsedTime.tsv

* Indicates how long it took for each feature-selection algorithm to execute.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/Nested_FeatureSelection_ElapsedTime.tsv)

## Log.txt

* Contains the text that was printed to Standard output. 
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/Log.txt)
