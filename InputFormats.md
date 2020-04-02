# Input File Formats

ShinyLearner uses a file's extension to determine how it will parse input files. Currently ShinyLearner supports the following file extensions: ```.tsv```, ```.ttsv```, ```.csv```, ```.tcsv```, and ```.arff```. Each has a unique way of organizing data. An *instance* (sample) is an individual or entity that has been observed, while a feature (variable) is one type of measurement collected for that instance. For example, instances could be medical patients, and features could be measurements that have been collected for each patient--such as age, height, sex, and so forth. The row or column that identifies the instance's class must be named 'Class'. Input files may be gzipped; if so, ShinyLearner assumes that '.gz' has been appended to the file name.

## Tab-Separated Values File (.tsv)

* Rows are instances.
* Columns are features.
* Values are separated by tab characters.
* The first column should contain unique identifiers for each instance.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/StrongSignal_Both.tsv)

## Transposed Tab-Separated Values File (.ttsv)

* Columns are instances.
* Rows are features.
* Values are separated by tab characters.
* The first row should contain unique identifiers for each instance.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/StrongSignal_Both.ttsv)

## Comma-Separated Values File (.csv)

* Rows are instances.
* Columns are features.
* Values are separated by commas.
* The first column should contain unique identifiers for each instance.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/StrongSignal_Both.csv)

## Transposed Comma-Separated Values File (.tcsv)

* Columns are instances.
* Rows are features.
* Values are separated by commas.
* The first row should contain unique identifiers for each instance.
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/StrongSignal_Both.tcsv)

## Attribute-Relation File Format (.arff)

* Header section: Each row describes one feature.
* Data section: Each row describes one instance and its data as comma-separated values (sorted by the order of features described in the header).
* Values are separated by commas.
* For full explanation, visit [http://www.cs.waikato.ac.nz/ml/weka/arff.html](http://www.cs.waikato.ac.nz/ml/weka/arff.html).
* [Example](https://github.com/srp33/ShinyLearner/blob/master/Validation/ExampleFiles/StrongSignal_Both.arff)

* Please [log an issue](https://github.com/srp33/ShinyLearner/issues) on GitHub if you would like to request support for an additional data format in ShinyLearner.
