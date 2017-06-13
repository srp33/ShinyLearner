# Output Data Files

ShinyLearner produces output files that follows the principles of [tidy data](http://vita.had.co.nz/papers/tidy-data.pdf). This affords extra flexibility and consistency when interpreting the results. These tab-delimited text files can be imported directly into third-party analytic tools, such as Microsoft Excel, R or Python, for further analysis. The descriptions below indicate what each output file contains. The [UserScripts documentation](https://github.com/srp33/ShinyLearner/tree/master/UserScripts/docs) indicates which output files are produced by each type of analysis.

## Metrics.tsv

* Indicates various [classification accuracy measures](https://github.com/srp33/ShinyLearner/blob/master/Metrics.md).
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/Metrics.tsv)

## Predictions.tsv

* Contains individual-level predictions for each sample/instance for which predictions were made for each algorithm.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/Predictions.tsv)

## SelectedFeatures.tsv

* A ranked list of features for each feature-selection algorithm.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/SelectedFeatures.tsv)

## SelectedFeatures_Summarized.tsv

* A ranked list of features, averaged (Borda count) across all feature-selection algorithms used.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/SelectedFeatures_Summarized.tsv)

## ElapsedTime.tsv

* Indicates how long it took for each algorithm to execute.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/Elapsed.tsv)

When nested cross validation is used to optimize algorithm or feature selection, ShinyLearner produces output files that describe algorithm performance within the training sets used for optimization. The following descriptions indicate what these files contain.

## Nested_Metrics.tsv

* Indicates various [classification accuracy measures](https://github.com/srp33/ShinyLearner/blob/master/Metrics.md).
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/Nested_Metrics.tsv)

## Nested_Predictions.tsv

* Contains individual-level predictions for each sample/instance for which predictions were made for each algorithm.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/Nested_Predictions.tsv)

## Nested_SelectedFeatures.tsv

* A ranked list of features for each feature-selection algorithm.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/Nested_SelectedFeatures.tsv)

## Nested_SelectedFeatures_Summarized.tsv

* A ranked list of features, averaged (Borda count) across all feature-selection algorithms used.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/Nested_SelectedFeatures_Summarized.tsv)

## Nested_Classification_ElapsedTime.tsv

* Indicates how long it took for each classification algorithm to execute.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/Nested_Classification_ElapsedTime.tsv)

## Nested_FeatureSelection_ElapsedTime.tsv

* Indicates how long it took for each feature-selection algorithm to execute.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/Nested_FeatureSelection_ElapsedTime.tsv)

## Log.txt

* Standard output from the terminal. 
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/Log.txt)
