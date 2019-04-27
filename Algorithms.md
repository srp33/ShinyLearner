ShinyLearner incorporates classification and feature-selection algorithms from third-party machine-learning libraries. You can see which algorithms and hyperparameters are currently supported if you examine the [AlgorithmScripts](https://github.com/srp33/ShinyLearner/tree/master/AlgorithmScripts) directory on GitHub. The [Classification](https://github.com/srp33/ShinyLearner/tree/master/AlgorithmScripts/Classification) directory contains subdirectories called [arff/weka](https://github.com/srp33/ShinyLearner/tree/master/AlgorithmScripts/Classification/arff/weka), [tsv/keras](https://github.com/srp33/ShinyLearner/tree/master/AlgorithmScripts/Classification/tsv/keras), [tsv/mlr](https://github.com/srp33/ShinyLearner/tree/master/AlgorithmScripts/Classification/tsv/mlr), and [tsv/sklearn](https://github.com/srp33/ShinyLearner/tree/master/AlgorithmScripts/Classification/tsv/sklearn). Within each of these subdirectories, you will find a series of additional subdirectories with the names of algorithms that are available in ShinyLearner. For example, the [arff/weka](https://github.com/srp33/ShinyLearner/tree/master/AlgorithmScripts/Classification/arff/weka) subdirectory contains a [RandomForest](https://github.com/srp33/ShinyLearner/tree/master/AlgorithmScripts/Classification/arff/weka/RandomForest) subdirectory, which contains script(s) that enable ShinyLearner to execute this algorithm. If you would like to see the hyperparameters that ShinyLearner will use, examine these scripts. The script whose name starts with `default` containers the hyperparameter values that we consider to be defaults; these may not always coincide with defaults used in the third-party software.

*Important*: ShinyLearner provides support for a wide range of algorithms and hyperparameters. However, there are endless possibilities of what else it could support. We are open to your [suggestions](https://github.com/srp33/ShinyLearner/issues).

If you would like to learn more about the third-party machine-learning libraries used in ShinyLearner, please visit the links below.

## Classification algorithms

* [Weka](http://weka.sourceforge.net/packageMetaData/)
* [keras](https://mlr-org.github.io/keras/)
* [mlr](https://mlr-org.github.io/mlr/)
* [scikit-learn](http://scikit-learn.org/stable/supervised_learning.html#supervised-learning)

## Feature-selection algorithms

* [Weka](http://weka.sourceforge.net/packageMetaData/)
* [mlr](https://mlr-org.github.io/mlr/)
* [scikit-learn](http://scikit-learn.org/stable/modules/feature_selection.html#feature-selection)
