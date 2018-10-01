## Installing software

To execute analyses using ShinyLearner, you will need to [install the Docker software](https://docs.docker.com/engine/installation) appropriate for your operating system. That is the only software you need to install!

## Preparing data

You will need to prepare input data in one of the [file formats](https://github.com/srp33/ShinyLearner/blob/master/InputFormats.md) supported by ShinyLearner.

## Executing the analysis

Once you have prepared your data, you need to select the algorithm(s) and settings that ShinyLearner will use for your analysis. We have created a [graphical user interface](http://shinylearner.byu.edu/shinylearnerweb/) that simplifies this process. This web-based tool asks you to indicate the name(s) of your input files, the algorithm(s) to execute, which validation strategy to use, etc. Based on the options you choose, it will generate a Docker command, which you can execute at the command line. ShinyLearner (and Docker) will take care of the rest.

## Analyzing the output

After ShinyLearner has finished executing an analysis, it will produce a series of tab-delimited output files. [Here](https://github.com/srp33/ShinyLearner/blob/master/OutputFiles.md) you can learn more about what these files contain and how to interpret them.

Please [contact us](https://github.com/srp33/ShinyLearner/blob/master/Contact.md) with any questions or suggestions you may have.
