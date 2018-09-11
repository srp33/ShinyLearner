ShinyLearner incorporates classification and feature-selection algorithms from several third-party machine-learning libraries (see below). You can see which algorithms are currently supported by examining the [AlgorithmScripts directory](https://github.com/srp33/ShinyLearner/tree/master/AlgorithmScripts) on GitHub. The [Classification](https://github.com/srp33/ShinyLearner/tree/master/AlgorithmScripts/Classification) directory contains subdirectories called [arff/weka](https://github.com/srp33/ShinyLearner/tree/master/AlgorithmScripts/Classification/arff/weka), [tsv/mlr](https://github.com/srp33/ShinyLearner/tree/master/AlgorithmScripts/Classification/tsv/mlr), and [tsv/sklearn](https://github.com/srp33/ShinyLearner/tree/master/AlgorithmScripts/Classification/tsv/sklearn). Within each of these subdirectories, you will find a series of additional subdirectories that are the names of algorithms that are available to execute in ShinyLearner. For example, the [arff/weka](https://github.com/srp33/ShinyLearner/tree/master/AlgorithmScripts/Classification/arff/weka) subdirectory contains a [RandomForest](https://github.com/srp33/ShinyLearner/tree/master/AlgorithmScripts/Classification/arff/weka/RandomForest) subdirectory, which contains script(s) that enable ShinyLearner to execute this algorithm. If you would like to see the exact parameters that ShinyLearner will use, examine these scripts. (There is a similar directory structure for [feature-selection algorithms](https://github.com/srp33/ShinyLearner/tree/master/AlgorithmScripts/FeatureSelection).)

If you would like to learn more about the third-party libraries, please visit the links below.

## Classification algorithms

* [scikit-learn](http://scikit-learn.org/stable/supervised_learning.html#supervised-learning)
* [Weka](http://weka.sourceforge.net/packageMetaData/)
* [mlr](http://mlr-org.github.io/mlr-tutorial/release/html/integrated_learners/index.html)

## Feature selection algorithms

* [scikit-learn](http://scikit-learn.org/stable/modules/feature_selection.html#feature-selection)
* [Weka](http://weka.sourceforge.net/packageMetaData/)
* [mlr](https://mlr-org.github.io/mlr/articles/mlr.html
