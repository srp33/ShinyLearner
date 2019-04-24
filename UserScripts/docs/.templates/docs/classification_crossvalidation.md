**DESCRIPTION**

This `classification_crossvalidation` command executes the specified algorithm(s) using a k-fold cross-validation strategy. It performs classification (but not feature selection or hyperparameter optimization).

**REQUIRED ARGUMENTS**

{args/data}
{args/description}
{args/output-dir}
{args/folds}
{args/iterations}
{args/classif-algo}

{descriptions/data}

{descriptions/description}

{descriptions/output-dir}

{descriptions/folds}

{descriptions/iterations}

{descriptions/classif-algo}

{descriptions/multiple}

**OPTIONAL ARGUMENTS**

{args/verbose}
{args/ohe}
{args/scale}
{args/impute}
{args/num-cores}
{args/temp-dir}

{descriptions/verbose}

{descriptions/ohe}

{descriptions/scale}

{descriptions/impute}

{descriptions/num-cores}

{descriptions/temp-dir}

**OUTPUT FILES**

{descriptions/output_files_intro}

* Metrics.tsv

* Predictions.tsv

* ElapsedTime.tsv

* Log.txt

**EXAMPLE**

{examples/intro}
{examples/iterations}
{examples/folds}
{examples/classif-algo}
{examples/scale}