## Incorporating new classification algorithms into ShinyLearner

ShinyLearner can be extended to use classification algorithms that are not yet supported. The key requirement is that the algorithm must be executable via a [bash script](https://ryanstutorials.net/bash-scripting-tutorial/bash-script.php). ShinyLearner takes care of splitting the data into training/testing sets, reformatting the data, etc. When executing a classification algorithm, it passes a training-data file (with class labels) and a test-data file (no class labels) to your bash script. That bash script should then load the data, train the algorithm, and make predictions for each test sample (more details below). In most cases, this logic would be performed using a programming language like Python, R, or C++. The bash script simply passes those values from ShinyLearner to your algorithm.

Typically, classification algorithms support a set of [hyperparameters](https://en.wikipedia.org/wiki/Hyperparameter_(machine_learning)), which influence the algorithm's behavior. The user might wish to try various values for these hyperparameters to see what produces the highest accuracy (they should do this within a training set). ShinyLearner supports such parameter optimization via nested cross validation. When you incorporate a new algorithm into ShinyLearner, you will need to provide a bash script that uses default hyperparameter values for your algorithm. Then you could also provide additional bash scripts that use alternate hyperparameter values.

Each bash script should accept the following arguments:

1. A path to the training-data file.
2. A path to the test-data file.
3. A comma-separated list of class values. When your algorithm makes probabilistic predictions, it needs to keep track of which class is associated with each probability value. So it tells you the order in which those predictions should be printed in the output.
4. The number of CPU cores that should be used by your algorithm. This will be an integer of 1 or greater. If your algorithm supports multi-core execution, please use it (based on the number of cores specified).
5. A value of "true" or "false" that indicates whether to print verbose messages (to enable troubleshooting).

[Here](https://github.com/srp33/ShinyLearner/tree/master/AlgorithmScripts/Classification/tsv/demo_library/demo_algorithm) you can find an example implementation, including example bash scripts, input/output files, etc.

After you have created scripts for your algorithm, please do the following:

1. Identify any software dependencies that are necessary to execute your scripts. This might include third-party machine-learning libraries or more generic dependencies. Software already included in ShinyLearner can be found [here](https://github.com/srp33/ShinyLearner_Environment/blob/master/Dockerfile). If you need to add dependencies, [clone](https://help.github.com/articles/cloning-a-repository/) [this repository](https://github.com/srp33/ShinyLearner_Environment) and modify the Dockerfile in [this repository](https://github.com/srp33/ShinyLearner_Environment) so that it installs the needed dependencies. Then submit a GitHub [pull request](https://github.com/srp33/ShinyLearner_Environment/pulls) with these changes. (See tutorial [here](https://help.github.com/articles/about-pull-requests/)). We will review and test these changes.

2. Clone the main ShinyLearner [repository](https://github.com/srp33/ShinyLearner). Navigate to the ```AlgorithmScripts/Classification/tsv``` directory. Within that directory, create a new directory that describes the *category* of algorithm that you created. Within *that* directory, create a subdirectory named after the specific algorithm you are adding. For example, in ```AlgorithmScripts/Classification/tsv```, there is a directory called ```sklearn```. This category of algorithms includes all those from the [scikit-learn](http://scikit-learn.org) library that are included in ShinyLearner. Within the ```sklearn``` directory, there is a subdirectory for each of these algorithms.

3. Within the subdirectory that you just created, provide a bash script for each hyperparameter combination that you want to support. The script that uses default parameters should start with ```default__```. All other scripts should start with ```alt__```. Please use script names that are as descriptive as possible. Within this subdirectory, you would also include any code/binary files that are needed to execute your script.

4. Submit a [pull request](https://github.com/srp33/ShinyLearner/pulls) with these changes.