# Output Data Files

ShinyLearner follows the principles of [tidy data](http://vita.had.co.nz/papers/tidy-data.pdf). This affords extra flexibility when interpreting the results. These tab-delineated text files can be imported directly into third-party analytic tools--such as Microsoft Excel or R--for further analysis.

## Metrics.tsv

* There are various measures to interpret prediction accuracy. For a comprehensive list [see here](https://github.com/srp33/ShinyLearner/blob/master/Metrics.md).
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/Metrics.tsv)

## Predictions.tsv

* Describes individual-level predictions for each instance that was analyzed.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/Predictions.tsv)

## Benchmark.tsv

* ShinyLearner records the runtimes for each the prediction in the experiment.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/Benchmark.tsv)

## SelectedFeatures.tsv

* Selected features for the analyses.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/SelectedFeatures.tsv)


## SelectedFeatures_Summarized_Nested.tsv

* Mean ranking of features across internal validation folds.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/SelectedFeatures_Summarized_Nested.tsv)

## Nested Prefix

* Output files with the "Nested" prefix include data for the internal validation folds. 
* [Nested Metrics Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/NestedMetricsFile.tsv)
* [Nested Predictions Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/NestedPredictionsFile.tsv)
* [Nested Benchmarks Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/NestedBenchmarkFile.tsv)
* [Nested Selected Features Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/NestedSelectedFeaturesFile.tsv)

## Log.txt

* Output from the terminal. 
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/Log.txt)

