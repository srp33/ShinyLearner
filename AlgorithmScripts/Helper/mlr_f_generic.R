numArgs <- length(commandArgs())

dataFilePath <- commandArgs()[numArgs - 2]
numCores <- as.integer(commandArgs()[numArgs - 1])
algorithm <- commandArgs()[numArgs]
#parameterDescription <- commandArgs()[9]

suppressPackageStartupMessages(suppressWarnings(library(mlr)))
suppressPackageStartupMessages(library(methods))

if (numCores > 1)
{
  suppressPackageStartupMessages(suppressWarnings(library(parallelMap)))
  parallelStartSocket(2)
}

data <- read.table(dataFilePath, sep="\t", stringsAsFactors = TRUE, header=TRUE, row.names = 1, check.names=FALSE)

columnNames <- colnames(data)
classIndex <- which(columnNames=="Class")
modColumnNames <- paste("Column", 1:ncol(data), sep="")
modColumnNames[classIndex] <- "Class"
colnames(data) <- modColumnNames

task <- makeClassifTask(data = data, target = "Class")

learn <- function(parameterList)
{
  set.seed(0)

  # Dynamically execute the code for the specified algorithm and parameters.
  code = paste0("fv = suppressWarnings(generateFilterValuesData(task, method = ", algorithm, ")$data)")
  eval(parse(text = paste0("fv = suppressWarnings(generateFilterValuesData(task, method = ", algorithm, ")$data)")))

  fv[,1] = columnNames[-classIndex]
  fv <- fv[order(fv$value, decreasing=TRUE),,drop=FALSE]

  features <- paste(fv[,1], collapse=",")
  output <- t(as.data.frame(features))

  write.table(output, "", sep="\t", row.names = FALSE, col.names=FALSE, quote = FALSE)
}

#if (parameterDescription == "default") {
  #learn(NULL, "")
  learn(list())
#} else {
#  parameterData <- read.table(parametersFilePath, sep="\t", header=TRUE, stringsAsFactor=F, row.names=NULL, check.names=FALSE, quote="")
#  parameterNames <- colnames(parameterData)
#
#  for (i in 1:nrow(parameterData))
#  {
#    parameterList <- list()
#    parameterList[["task"]] <- task
#    parameterList[["method"]] <- algorithm
#
#    for (j in 1:ncol(parameterData))
#      parameterList[[parameterNames[j]]] <- parameterData[i,j]
#
#    parameterDescription <- paste(paste(parameterNames, parameterData[i,], sep="="), collapse=";")
#
#    learn(parameterList, parameterDescription)
#  }
#}

if (numCores > 1)
  parallelStop()
