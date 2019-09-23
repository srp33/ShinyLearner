## Installing software

To execute ShinyLearner, you will need to install the [Docker engine](https://docs.docker.com/engine/installation). If you would like to use graphical processing units, you must also install [nvidia-docker](https://github.com/NVIDIA/nvidia-docker).

## Preparing data

You will need to prepare input data in one of the [file formats](https://github.com/srp33/ShinyLearner/blob/master/InputFormats.md) supported by ShinyLearner.

## Executing the analysis

Once you have prepared the data, you will need to select the algorithm(s) and settings that ShinyLearner will use for your analysis. We have created a [graphical user interface](https://bioapps.byu.edu/shinylearner) that simplifies this process. This web-based tool asks you to indicate the name(s) of your input files, the algorithm(s) to execute, which validation strategy to use, etc. Based on the options you choose, it will generate a Docker command, which you can execute at the command line. ShinyLearner (and Docker) will take care of the rest.

Alternatively, you can see examples of how to execute analyses at the following pages:

* [Basic k-fold cross validation](https://github.com/srp33/ShinyLearner/blob/master/UserScripts/docs/classification_crossvalidation.md)
* [Basic Monte Carlo cross validation](https://github.com/srp33/ShinyLearner/blob/master/UserScripts/docs/classification_montecarlo.md)
* [Nested k-fold cross validation](https://github.com/srp33/ShinyLearner/blob/master/UserScripts/docs/nestedclassification_crossvalidation.md)
* [Nested Monte Carlo cross validation](https://github.com/srp33/ShinyLearner/blob/master/UserScripts/docs/nestedclassification_montecarlo.md)
* [Nested k-fold cross validation with feature selection](https://github.com/srp33/ShinyLearner/blob/master/UserScripts/docs/nestedboth_crossvalidation.md)
* [Nested Monte Carlo cross validation with feature selection](https://github.com/srp33/ShinyLearner/blob/master/UserScripts/docs/nestedboth_montecarlo.md)

## Analyzing the output

After ShinyLearner has finished executing an analysis, it will produce a series of tab-delimited text files. [Here](https://github.com/srp33/ShinyLearner/blob/master/OutputFiles.md) you can learn more about what these files contain and how to interpret them.

Please [contact us](https://github.com/srp33/ShinyLearner/blob/master/Contact.md) with any questions or suggestions you may have.
