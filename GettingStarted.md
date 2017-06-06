## Installation

To execute analyses using ShinyLearner, you will need to [install the Docker software](https://docs.docker.com/engine/installation) appropriate for your operation system. That is the only software you need to install!

## Executing ShinyLearner

Next you will need to prepare your input data in one of the file formats supported by ShinyLearner: ```.csv```, ```.tsv```, ```.tcsv```, ```.ttsv```, or ```.arff```.

A ```.csv``` file would contain comma-separated values. Instances would be represented as rows, features (independent variables) would be represented as columns. A ```.tsv``` file would have the same structure as a ```.csv``` file, but values would be separated by tabs rather than commas. The ```.arff``` file format is described [here](http://www.cs.waikato.ac.nz/ml/weka/arff.html). No matter what format you use, your input data should contain one feature called "Class" that contains the class (dependent-variable) values. Below is an example.

#### .csv example input file

```
InstanceID,FeatureA,FeatureB,FeatureC,Class
Instance1,1.23,3.45,4.56,-1
Instance2,0.98,8.76,7.65,-1
Instance3,2.21,5.42,9.90,1
Instance4,1.74,6.65,8.81,1
```

See [InputFormats.md](https://github.com/srp33/ShinyLearner/blob/master/InputFormats.md) for more information about input-data formats.

#### Specifying parameters

Your data can be split across multiple input data files. ShinyLearner will identify instance identifiers that overlap between these files and perform an analysis on those overlapping instances.

Below is a description of the parameters that you would specify, in the order you would specify them, to perform a classification analysis (*without* feature selection) using Monte Carlo cross-validation.

1. Path to the input data file(s). Wildcards are allowed (surround by quotes). You can also specify multiple paths, separated by commas. Input files can be gzipped. Example: ```InputData/MyData.csv.gz```.
2. A short, text-based description of the analysis (no spaces allowed). Example: ```My_Interesting_Analysis```.
3. The number of Monte Carlo iterations. Example: ```10```.
4. The number of *internal* cross-validation iterations. These iterations are used to optimize selection of algorithm(s) and hyperparameter(s). Example ```5```.
5. Whether to show debug information. Example: ```false```. Alternative: ```true```.
6. The algorithm(s) that should be executed. Wildcards are allowed. All available algorithms can be found within the ShinyLearner [code base](https://github.com/srp33/ShinyLearner/tree/master/AlgorithmScripts/Classification). Example: ```AlgorithmScripts/Classification/arff/weka/SVM*/default```.
7. Path to an output file that will contain predictions for each instance. Example: ```OutputData/Predictions.tsv```.
8. Path to an output file that will contain performance metrics for each algorithm. Example: ```OutputData/Metrics.tsv```.
9. Path to an output file that will contain predictions for each instance for *internal* cross-validation iterations. Example: ```OutputData/InternalPredictions.tsv```.
10. Path to an output file that will contain performance metrics for each algorithm for *internal* cross-validation iterations. Example: ```OutputData/InternalMetrics.tsv```.
11. Path to an output file that will contain benchmark values (the length of time it takes for each algorithm to execute) for *internal* cross-validation iterations. Example: ```OutputData/InternalBenchmark.tsv```.
12. Path to a log file that will be created. Example: ```OutputData/log```.

([See here](https://github.com/srp33/ShinyLearner/blob/master/OutputFiles.md) for information about the formatting of these output files.)

#### Example

Below is an example of how you would execute the analysis, using the above parameters, at the command line, from a UNIX-based operating system. Note that you also need to *share* the directories that will contain your input and output files with the Docker container. This will enable Docker to see your input files and store your output files outside of the container. This is done via the ```-v``` parameter. The ```-v``` parameter can be specified multiple times.

```
sudo docker run --rm \
  -v $(pwd)/InputData:/InputData \
  -v $(pwd)/OutputData:/OutputData \
  srp33/shinylearner:version255 \
  /UserScripts/nestedclassification_montecarlo \
  InputData/MyData.csv.gz \
  My_Interesting_Analysis \
  10 \
  5 \
  false \
  "AlgorithmScripts/Classification/arff/weka/SVM*/default" \
  OutputData/Predictions.tsv \
  OutputData/Metrics.tsv \
  OutputData/Internal_Predictions.tsv \
  OutputData/Internal_Metrics.tsv \
  OutputData/Internal_Benchmark.tsv \
  OutputData/Test.log
```

#### Web interface

To make it easier for our users to specify parameters and build these commands, we have created a [graphical user interface](http://shinylearner.byu.edu) that simplifies this process.

Please [contact us](https://github.com/srp33/ShinyLearner/blob/master/Contact.md) with any questions or suggestions you may have.
