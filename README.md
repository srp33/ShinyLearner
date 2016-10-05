![ShinyLearner logo](Web/shinylearner/www/Logo_Small.jpg)

==========================
[![Build Status](https://travis-ci.org/srp33/ShinyLearner.svg?branch=master)](https://travis-ci.org/srp33/ShinyLearner)

## Introduction

ShinyLearner is a software framework for performing machine-learning classification in a flexible and tidy manner. It includes 30+ machine-learning algorithms accross multiple libraries.

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
