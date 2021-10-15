dataFilePath <- commandArgs()[7]
algorithm <- commandArgs()[8]

suppressPackageStartupMessages(library(mlr))
suppressPackageStartupMessages(library(methods))

data <- read.table(dataFilePath, sep="\t", stringsAsFactors = TRUE, header=TRUE, row.names = 1, check.names=FALSE)

task.lrn = makeClassifTask(data = data, target = "Class")

set.seed(0)

if (algorithm == "permutation.importance") {
  fv = generateFilterValuesData(task.lrn, method = algorithm, learner="classif.logreg")$data
} else {
  fv = generateFilterValuesData(task.lrn, method = algorithm)$data
}

fv <- fv[order(fv[,algorithm], decreasing=TRUE),,drop=FALSE]

write.table(fv$name, "", sep="\t", row.names = FALSE, col.names=FALSE, quote = FALSE)
