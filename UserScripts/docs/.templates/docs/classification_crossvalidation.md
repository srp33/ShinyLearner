## DESCRIPTION

The `classification_crossvalidation` command uses k-fold cross-validation. It performs classification (but not hyperparameter optimization or feature selection).

## REQUIRED ARGUMENTS

{args/data}
{args/description}
{args/folds}
{args/iterations}
{args/classif-algo}

{descriptions/data}

{descriptions/description}

{descriptions/folds}

{descriptions/iterations}

{descriptions/classif-algo}

{descriptions/multiple_cl}

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

* Metrics.tsv

* Predictions.tsv

* ElapsedTime.tsv

* Log.txt

## EXAMPLE

{examples/intro}
      UserScripts/classification_crossvalidation \
{examples/data}
{examples/description}
{examples/iterations}
{examples/folds}
{examples/classif-algo}
{examples/seed}
{examples/scale}
