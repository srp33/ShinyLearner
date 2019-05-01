## DESCRIPTION

The `nestedclassification_crossvalidation` command uses k-fold cross-validation. It performs classification and hyperparameter optimization (but not feature selection). It uses nested, k-fold cross validation for hyperparameter optimization. It outputs the performance of each algorithm for the inner (nested) folds and uses a select-best method for predictions in the outer folds.

## REQUIRED ARGUMENTS

{args/data}
{args/description}
{args/outer-folds}
{args/inner-folds}
{args/iterations}
{args/classif-algo}

{descriptions/data}

{descriptions/description}

{descriptions/outer-folds}

{descriptions/inner-folds}

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

* Nested_Metrics.tsv

* Nested_Predictions.tsv

* Nested_ElapsedTime.tsv

* ElapsedTime.tsv

* Log.txt

## EXAMPLE

{examples/intro}
      UserScripts/nestedclassification_crossvalidation \
{examples/data}
{examples/description}
{examples/iterations}
{examples/outer-folds}
{examples/inner-folds}
{examples/classif-algo}
{examples/seed}
{examples/scale}
