# Input Data File Formats

ShinyLearner uses convention over configuration. In other words, the file extension determines how ShinyLearner will parse the files. Currently ShinyLearner supports five different file extensions including ```.tsv```, ```.ttsv```, ```.csv```, ```.tcsv```, and ```.arff```. Each has a unique way of organizing instances and features. An *instance* is a single observation in the data set, while a feature is one type of measurement on that instance. For example, an instance could be a patient, and that patient may have data accros multiple features such as age, height, sex, and so forth. One of the features must be named 'Class'. Input files may be gzipped (append '.gz' to file name).

## Tab-Separated Values File (.tsv)

* Rows are Instances
* Columns are Features
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/StrongSignal_Both.tsv)

## Transposed Tab-Separated Values File (.ttsv)

* Columns are Instances
* Rows are Features
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/StrongSignal_Both.ttsv)

## Comma-Separated Values File (.csv)

* Rows are Instances
* Columns are Features
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/StrongSignal_Both.csv)

## Transposed Comma-Separated Values File (.tcsv)

* Columns are Instances
* Rows are Features
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/StrongSignal_Both.tcsv)

## Attribute-Relation File Format (.arff)

* Header Section: Each row describes one feature
* Data Section: Each row describes one instance and its data as comma-separated values (sorted by the order of features described in the header)
* For full explanation visit, [http://www.cs.waikato.ac.nz/ml/weka/arff.html](http://www.cs.waikato.ac.nz/ml/weka/arff.html)
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/StrongSignal_Both.arff)
