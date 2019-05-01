## DESCRIPTION

The `featureselection_montecarlo` command uses Monte Carlo cross-validation. It performs feature selection (but not classification). It outputs a ranked list of features for each algorithm as well as a Borda Count list of features based on the rankings of all feature-selection algorithms.

## REQUIRED ARGUMENTS

{args/data}
{args/description}
{args/iterations}
{args/fs-algo}

{descriptions/data}

{descriptions/description}

{descriptions/iterations}

{descriptions/fs-algo}

{descriptions/multiple_fs}

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

* SelectedFeatures.tsv

* SelectedFeatures_Summarized.tsv

* ElapsedTime.tsv

* Log.txt

## EXAMPLE

{examples/intro}
      UserScripts/featureselection_montecarlo \
{examples/data}
{examples/description}
{examples/iterations}
{examples/fs-algo}
{examples/seed}
{examples/scale}
