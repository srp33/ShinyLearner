## DESCRIPTION

The `nestedboth_montecarlo` command uses Monte Carlo cross-validation. It performs classification and can perform hyperparameter optimization as well as feature selection. It uses nested, Monte Carlo cross validation for hyperparameter optimization and feature selection. It outputs the performance of each algorithm for the inner (nested) folds and uses a select-best method for predictions in the outer folds. It also outputs a ranked list of features for each feature-selection algorithm as well as a Borda Count list of features based on the rankings of all feature-selection algorithms.

## REQUIRED ARGUMENTS

{args/data}
{args/description}
{args/outer-iterations}
{args/inner-iterations}
{args/classif-algo}
{args/fs-algo}
{args/num-features}

{descriptions/data}

{descriptions/description}

{descriptions/outer-iterations}

{descriptions/inner-iterations}

{descriptions/classif-algo}

{descriptions/fs-algo}

{descriptions/num-features}

{descriptions/multiple_clfs}

## OPTIONAL ARGUMENTS

{args/verbose}
{args/seed}
{args/train-proportion}
{args/ohe}
{args/scale}
{args/impute}
{args/num-cores}
{args/temp-dir}

{descriptions/verbose}

{descriptions/seed}

{descriptions/train-proportion}

{descriptions/ohe}

{descriptions/scale}

{descriptions/impute}

{descriptions/num-cores}

{descriptions/temp-dir}

## OUTPUT FILES

{descriptions/output_files_intro}

* Metrics.tsv

* Predictions.tsv

* SelectedFeatures.tsv

* Nested_Metrics.tsv

* Nested_Predictions.tsv

* Nested_SelectedFeatures.tsv

* Nested_SelectedFeatures_Summarized.tsv

* Nested_Classification_ElapsedTime.tsv

* Nested_FeatureSelection_ElapsedTime.tsv

* Log.txt

## EXAMPLE

{examples/intro}
      UserScripts/nestedboth_montecarlo \
{examples/data}
{examples/description}
{examples/outer-iterations}
{examples/inner-iterations}
{examples/classif-algo}
{examples/fs-algo}
{examples/seed}
{examples/num-features}
{examples/scale}
