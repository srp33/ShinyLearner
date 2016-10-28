#Below is a simple example of how to execute *ShinyLearner* for a basic classification analysis using [Monte Carlo cross-validation](https://en.wikipedia.org/wiki/Cross-validation_(statistics)#Repeated_random_sub-sampling_validation). It uses the test data files present in the Validation folder.
#
#```
dataFiles=/Validation/StrongSignal_Both.tsv.gz
description=ValidationTest
numIterations=10
debug=false
classifAlgos="/AlgorithmScripts/Classification/arff/weka/Random*/default"
outPredictionsFile="/Validation/Test_Predictions.tsv"
outMetricsFile="/Validation/Test_Metrics.tsv"
outBenchmarkFile="/Validation/Test_Benchmark.tsv"
outLogFile="/Validation/Test.log"

echo sudo docker run --rm --name inputdata -v $(pwd)/Validation:/Validation srp33/shinylearner:version205 /UserScripts/classification_montecarlo "$dataFiles" "$description" "$numIterations" "$debug" "$classifAlgos" "$outPredictionsFile" "$outMetricsFile" "$outBenchmarkFile" "$outLogFile"
#```
