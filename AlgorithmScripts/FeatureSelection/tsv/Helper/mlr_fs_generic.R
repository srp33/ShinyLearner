dataFilePath <- commandArgs()[7]
algorithm <- commandArgs()[8]
parametersFilePath <- commandArgs()[9]

suppressPackageStartupMessages(library(mlr))
suppressPackageStartupMessages(library(methods))

data <- read.table(dataFilePath, sep="\t", stringsAsFactors = TRUE, header=TRUE, row.names = 1, check.names=FALSE)

task <- makeClassifTask(data = data, target = "Class")

learn <- function(parameterList, parameterDescription, ...)
{
  set.seed(0)

  if (algorithm == "permutation.importance") {
    fv = generateFilterValuesData(task, method = algorithm, learner="classif.logreg", ...)$data
  } else {
    fv = do.call(generateFilterValuesData, parameterList)$data
  }

  fv <- fv[order(fv[,algorithm], decreasing=TRUE),,drop=FALSE]
  fv <- cbind(parameterDescription, fv)

  write.table(fv[,1:2], "", sep="\t", row.names = FALSE, col.names=FALSE, quote = FALSE)
}

if (parametersFilePath == "") {
  learn(NULL, "")
} else {
  parameterData <- read.table(parametersFilePath, sep="\t", header=TRUE, stringsAsFactor=F, row.names=NULL, check.names=FALSE, quote="")
  parameterNames <- colnames(parameterData)

  for (i in 1:nrow(parameterData))
  {
    parameterList <- list()
    parameterList[["task"]] <- task
    parameterList[["method"]] <- algorithm

    for (j in 1:ncol(parameterData))
      parameterList[[parameterNames[j]]] <- parameterData[i,j]

    parameterDescription <- paste(paste(parameterNames, parameterData[i,], sep="="), collapse=";")

    learn(parameterList, parameterDescription)
  }
}
