## DESCRIPTION

The `classification_montecarlo` command uses Monte Carlo cross-validation. It performs classification (but not hyperparameter optimization or feature selection).

## REQUIRED ARGUMENTS

{args/data}
{args/description}
{args/iterations}
{args/classif-algo}

{descriptions/data}

{descriptions/description}

{descriptions/iterations}

{descriptions/classif-algo}

{descriptions/multiple_cl}

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

* ElapsedTime.tsv

* Log.txt

## EXAMPLE

{examples/intro}
      UserScripts/classification_montecarlo \
{examples/data}
{examples/description}
{examples/iterations}
{examples/classif-algo}
{examples/seed}
{examples/scale}
