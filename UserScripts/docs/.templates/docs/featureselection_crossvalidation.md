## DESCRIPTION

The `featureselection_crossvalidation` command uses k-fold cross-validation. It performs feature selection (but not classification). It outputs a ranked list of features for each algorithm as well as a Borda Count list of features based on the rankings of all feature-selection algorithms.

## REQUIRED ARGUMENTS

{args/data}
{args/description}
{args/iterations}
{args/folds}
{args/fs-algo}

{descriptions/data}

{descriptions/description}

{descriptions/iterations}

{descriptions/folds}

{descriptions/fs-algo}

{descriptions/multiple_fs}

## OPTIONAL ARGUMENTS

{args/verbose}
{args/seed}
{args/ohe}
{args/scale}
{args/impute}
{args/num-cores}
{args/temp-dir}

{descriptions/verbose}

{descriptions/seed}

{descriptions/ohe}

{descriptions/scale}

{descriptions/impute}

{descriptions/num-cores}

{descriptions/temp-dir}

## OUTPUT FILES

{descriptions/output_files_intro}

* SelectedFeatures.tsv

* SelectedFeatures_Summarized.tsv

* ElapsedTime.tsv

* Log.txt

## EXAMPLE

{examples/intro}
      UserScripts/featureselection_crossvalidation \
{examples/data}
{examples/description}
{examples/iterations}
{examples/folds}
{examples/fs-algo}
{examples/seed}
{examples/scale}
