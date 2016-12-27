## Incorporating new algorithms

ShinyLearner can be extended to support additional machine-learning algorithms. Users who wish to do this must do the following:

1. Identify any software dependencies that are necessary to support the algorithm. This might include third-party machine-learning libraries or more generic dependencies. Software already included in ShinyLearner can be found [here](https://github.com/srp33/ShinyLearner_Environment/blob/master/Dockerfile). If you need to add dependencies, [clone](https://help.github.com/articles/cloning-a-repository/) [this repository](https://github.com/srp33/ShinyLearner_Environment) and modify the Dockerfile so that it downloads and installs the needed dependencies.

2. Submit a GitHub [pull request](https://github.com/srp33/ShinyLearner_Environment/pulls). (See tutorial [here](https://help.github.com/articles/about-pull-requests/)). We will then review and test these changes.

3. Clone the main ShinyLearner GitHub [repository](https://github.com/srp33/ShinyLearner). Under *AlgorithmScripts*, you will find *Classification* and *FeatureSelection* directories. Navigate within these directories, depending on the type of algorithm you want to incorporate into ShinyLearner. These directories contain subdirectories that are named by convention, according to the required [input-data format](https://github.com/srp33/ShinyLearner/blob/master/InputFormats.md)for different algorithms. For example, Weka-implemented algorithms process algorithms in ```.arff``` format, so the Weka scripts in ShinyLearner are stored within ```ClassificationScripts/arff/weka```. [If your input format is not specified, please [contact us](https://github.com/srp33/ShinyLearner/blob/master/Contact.md).] Navigate to the directory associated with the input format that your algorithm will require. Then create a subdirectory with a representative name of the algorithm. Within that subdirectory, create a bash script called *default* that accepts specific arguments (see descriptions below) and invokes your algorithm. If you like, create additional bash scripts with representative names that use non-default parameters. You can find examples among the algorithms already included in ShinyLearer.

4. Submit a [pull request](https://github.com/srp33/ShinyLearner/pulls) with these changes. We will review and test these changes.

#### bash script arguments for classification algorithms

1. Path to input training data file.
2. Path to output training data file.
3. A sorted list of class values, separated by commas. (This ensures that all algorithms output predictions in the same order for the classes.)

#### bash script arguments for feature-selection algorithms

1. Path to input training data file.

Please [contact us](https://github.com/srp33/ShinyLearner/blob/master/Contact.md) with questions you may have.
