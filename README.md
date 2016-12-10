![ShinyLearner logo](Web/shinylearner/www/Logo_Small.jpg)

==========================
[![Build Status](https://travis-ci.org/srp33/ShinyLearner.svg?branch=master)](https://travis-ci.org/srp33/ShinyLearner)

## Introduction

*ShinyLearner* is a software framework for performing machine-learning classification in a flexible and tidy manner. It includes 30+ machine-learning algorithms accross multiple libraries.

## Quick Overview

With ShinyLearner, the user specifies input data files, classification algorithms, and validation strategies that she/he wants to use, and ShinyLearner takes care of the rest. No programming is required. After classification has been performed, ShinyLearner produces consistently formatted, "[tidy](http://vita.had.co.nz/papers/tidy-data.pdf)" data files that can be imported directly into third-party analytic tools--such as Microsoft Excel or [R](http://www.r-project.org/)--for further analysis. These data files specify predictions for each data instance and an array of evaluation metrics, including accuracy, sensitivity, specificity, positive predictive value, AUROC, etc. In addition, ShinyLearner indicates how long each algorithm took to execute, thus enabling analysts to evaluate accuracy improvements in context with computational efficiency.

## Features

* 30+ classification and feature selection algorithms from mlr, Sckit-Learn, and Weka
* [k-fold cross validation](https://en.wikipedia.org/wiki/Cross-validation_(statistics)#k-fold_cross-validation)
* [Monte-carlo cross validation](https://en.wikipedia.org/wiki/Cross-validation_(statistics)#Repeated_random_sub-sampling_validation)
* Nested optimization: parameters, features, and numbers of features are selected using internal cross-validation folds in a computationally efficient manner
* Ensemble-based aggregation of evidence across multiple classification algorithms
* Cross-platform Docker Container

## Why ShinyLearner?

#### Easy

One challenge of installing any software tool is to ensure that the tool functions properly on multiple operating systems and that the proper dependencies are installed. ShinyLearner and all its dependencies are encapsulated within a [Docker image](https://hub.docker.com/r/srp33/shinylearner). Accordingly, once a user has installed the [Docker software](https://www.docker.com), the user can install ShinyLearner and perform an analysis with a single command. These commands are executed via a command-line interface so that long-running analyses can be performed on computer clusters or in the cloud. To make it easier for users to build these commands, we have created a Web application that enables users to select parameters and construct ShinyLearner commands. This interface can be found [here](http://shinylearner.byu.edu) (currently it is a work in progress...).


#### Expandable

ShinyLearner can be extended to support additional machine-learning libraries or custom machine-learning scripts. Users who wish to do this must create a simple bash-script interface, identify any software dependencies, and create a [GitHub pull request](https://help.github.com/articles/about-pull-requests/).

#### Reliable

Each time new code (or scripts) have been committed to the ShinyLearner code repository, a [Travis CI continuous-integration build](https://travis-ci.org/srp33/ShinyLearner) is triggered. This build compiles the code and runs a series of tests to verify that each third-party algorithm is executable via ShinyLearner. In addition, it tests the performance of each algorithm (and parameter combination) on simulated data; these tests verify that the algorithms provide accurate predictions on easy-to-classify data and poor predictions on randomly shuffled data.

## How It Works

ShinyLearner acts as a software "wrapper" for existing machine-learning libraries, including [scikit-learn](http://scikit-learn.org/stable), [weka](http://www.cs.waikato.ac.nz/ml/weka), and [mlr](https://mlr-org.github.io/mlr-tutorial/release/html). Each of these libraries was written in a different programming language (Python, Java, and R, respectively). Scientists who wish to use these tools have been required to interface with them in a way that is specific to each library. For example, to use *scikit-learn* or *mlr*, users have needed to write code in the particular programming languages supported by these tools. Although *weka* provides a graphical user interface (in addition to a programming interface), users may find it difficult to extract and analyze predictions provided by this tool or to execute analyses at scale. A wide variety of classification algorithms are support by these tools, and there is some overlap across these libraries; however, many algorithms are implemented in only one of these packages. Therefore, to gain access to all the algorithms that a user may want to use, he/she may need to interface with multiple libraries. Additionally, if a scientist wanted to compare algorithms implemented in multiple libraries, considerable effort would be required. ShinyLearner makes this easy!

#### Machine-Learning

Machine-learning classification is an analytic technique used by data scientists within a variety of disciplines. Classification algorithms attempt to place data instances into known categories based on data observations. A classic example is the challenge of classifying [iris flowers](https://en.wikipedia.org/wiki/Iris_flower_data_set) into their correct species based on visually observable factors, such as petal length, petal width, sepal length, and sepal width. Rather than examine these factors individually, classification algorithms seek to identify multifactorial patterns within the data that discriminate the categories. Classification has been applied in various contexts, including computational biology, speech recognition, computer vision, spam filtering, credit scoring, etc. See more [here](https://en.wikipedia.org/wiki/Statistical_classification#Application_domains).

## Installation

To execute analyses using ShinyLearner, you will need to [install the Docker software](https://docs.docker.com/engine/installation) appropriate for your operation system. That is the only software you need to install!

## Executing ShinyLearner

Next you will need to prepare your input data in one of the file formats supported by ShinyLearner: ```.csv```, ```.tsv```, or ```.arff```.

A ```.csv``` file would contain comma-separated values. Instances would be represented as rows, features (independent variables) would be represented as columns. A ```.tsv``` file would have the same structure as a ```.csv``` file, but values would be separated by tabs rather than commas. The ```.arff``` file format is described [here](http://www.cs.waikato.ac.nz/ml/weka/arff.html). No matter what format you use, your input data should contain one feature called "Class" that contains the class (dependent-variable) values. Below is an example.

#### .csv example input file

```
InstanceID,FeatureA,FeatureB,FeatureC,Class
Instance1,1.23,3.45,4.56,-1
Instance2,0.98,8.76,7.65,-1
Instance3,2.21,5.42,9.90,1
Instance4,1.74,6.65,8.81,1
```

#### Specifying parameters

Your data can be split across multiple input data files. ShinyLearner will identify instance identifiers that overlap between these files and perform an analysis on those overlapping instances.

Below is a description of the parameters that you would specify, in the order you would specify them, to perform a basic classification analysis at the command line. (Additional examples and a user interface are forthcoming.)

1. Path to the input data file(s). Wildcards are allowed (surround by quotes). You can also specify multiple paths, separated by commas. Input files can be gzipped. Example: ```InputData/MyData.csv.gz```.
2. A short, text-based description of the analysis (no spaces allowed). Example: ```My_Interesting_Analysis```.
3. The number of Monte Carlo iterations. Example: ```l0```.
4. Whether to show debug information. Example: ```false```. Alternative: ```true```.
5. The algorithm(s) that should be executed. Wildcards are allowed. All available algorithms can be found within the ShinyLearner code base. Example: ```AlgorithmScripts/Classification/arff/weka/Random*/default```.
6. Path to an output file that will contain predictions for each instance. Example: ```OutputData/Predictions.tsv```.
7. Path to an output file that will contain performance metrics for each algorithm. Example: ```OutputData/Metrics.tsv```.
8. Path to an output file that will contain benchmark values (the length of time it takes for each algorithm to execute. Example: ```OutputData/Benchmark.tsv```.
9. Path to a log file that will be created. Example: ```OutputData/log```.

#### Example

Below is an example of how you would execute the analysis, using the above parameters, at the command line, from a UNIX-based operating system. Note that you also need to *share* the directories that will contain your input and output files with the Docker container. This will enable Docker to see your input files and store your output files outside of the container. This is done via the ```-v``` parameter. The ```-v``` parameter can be specified multiple times.

```
sudo docker run --rm \
  -v $(pwd)/InputData:/InputData \
  -v $(pwd)/OutputData:/OutputData \
  srp33/shinylearner:version233 \
  /UserScripts/classification_montecarlo \
  InputData/MyData.csv.gz \
  My_Interesting_Analysis \
  10 \
  false \
  "AlgorithmScripts/Classification/arff/weka/Random*/default" \
  OutputData/Test_Predictions.tsv \
  OutputData/Test_Metrics.tsv \
  OutputData/Test_Benchmark.tsv \
  OutputData/Test.log
```

We are working on additional examples. Please contact us with any suggestions about examples you may want. We are also working on a user interface to make it easier to specify these parameters.

## Adding your own algorithm

It is easy to integrate your own classification algorithm into ShinyLearner. To do so, you would complete the following steps:

1. Create a bash script that accepts the following arguments and performs classification:
  1. Path to input training data file.
  2. Path to output training data file.
  3. A sorted list of class values, separated by commas. (This ensures that all algorithms output predictions in the same order for the classes.)
2. Contact us with details about any additional software dependencies that need to be added to the ShinyLearner Docker environment to support execution of this script.
3. Create a pull request to merge this bash script into the ShinyLearner project. Algorithm scripts in ShinyLearner are specified by convention, depending on the expected input format of the algorithm. For example, Weka-implemented algorithms process algorithms in ```.arff``` format, so the Weka scripts in ShinyLearner are stored within ```ClassificationScripts/arff/weka```.

After validating your script, we will release a new version of ShinyLearner that includes your script in the master branch.

It is also possible to integrate your own feature-selection algorithm into ShinyLearner. The process is the same; however, your bash script only needs to support one parameter: a path to a training data file.

Let us know if you have any questions.
