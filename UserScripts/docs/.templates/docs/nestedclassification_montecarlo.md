## DESCRIPTION

The `nestedclassification_montecarlo` command uses Monte Carlo cross-validation. It performs classification and hyperparameter optimization (but not feature selection). It uses nested, Monte Carlo cross validation for hyperparameter optimization. It outputs the performance of each algorithm for the inner (nested) iterations and uses a select-best method for predictions in the outer iterations.

## REQUIRED ARGUMENTS

{args/data}
{args/description}
{args/output-dir}
{args/outer-iterations}
{args/inner-iterations}
{args/classif-algo}

{descriptions/data}

{descriptions/description}

{descriptions/output-dir}

{descriptions/outer-iterations}

{descriptions/inner-iterations}

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

* Nested_Metrics.tsv

* Nested_Predictions.tsv

* Nested_ElapsedTime.tsv

* Log.txt

## EXAMPLE

{examples/intro}
      UserScripts/nestedclassification_montecarlo \
{examples/data}
{examples/description}
{examples/output-dir}
{examples/outer-iterations}
{examples/inner-iterations}
{examples/classif-algo}
{examples/seed}
{examples/scale}
