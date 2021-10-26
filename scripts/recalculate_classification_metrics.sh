#! /bin/bash

# This script is specific to the Biomarker Benchmark Analysis.
# Used it to calculate AUPRC for that study.
# Can remove or simplify this script when done with that.

resultsDir="$1"

for predFile in $resultsDir/iteration*/*/Predictions.tsv
do
    if [ -f "$predFile" ]
    then
        echo "$predFile"

        metricsFile="$(dirname $predFile)/Metrics.tsv"

        if grep -q -wi AUPRC "$metricsFile"
        then
            echo AUPRC already calculated
        else
            Rscript --vanilla scripts/CalculateClassificationMetrics.R "$predFile" "$metricsFile"
        fi
    fi
done
