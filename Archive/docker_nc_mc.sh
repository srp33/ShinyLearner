#!/bin/bash
set -o errexit

dataFiles="$1"
description="$2"
tempOutDir=${description}
mkdir -p $tempOutDir
trap "echo Deleting $tempOutDir; rm -rf $tempOutDir" INT TERM EXIT
outerNumIterations="$3"
innerNumIterations="$4"
debug="$5"
classifAlgos="$6"
useDefaultParameters="$7"
outPredictionsFile="${tempOutDir}/Predictions.tsv"
outMetricsFile="${tempOutDir}/Metrics.tsv"
outBenchmarkFile="${tempOutDir}/Benchmarks.tsv"
outNestedPredictionsFile="${tempOutDir}/NestedPrediction.tsv"
outNestedMetricsFile="${tempOutDir}/NestedMetrics.tsv"
outNestedBenchmarkFile="${tempOutDir}/NestedBenchmarks.tsv"
class_options="$8"
exp_name="$9"

bash UserScripts/nestedclassification_montecarlo \
"$dataFiles" \
"$description" \
"$outerNumIterations" \
"$innerNumIterations" \
"$debug" \
"$classifAlgos" \
"$useDefaultParameters" \
"$outPredictionsFile" \
"$outMetricsFile" \
"$outBenchmarkFile" \
"$outNestedPredictionsFile" \
"$outNestedMetricsFile" \
"$outNestedBenchmarkFile"

echo "Render Results"
Rscript render_nc_mc.R \
"$tempOutDir" \
"$outerNumIterations" \
"$class_options" \
"$exp_name" \

mv ${tempOutDir}/${description}.html v/
tar -cf ${description}.tar ${tempOutDir}
gzip ${description}.tar
mv ${description}.tar.gz v/

