numArgs <- length(commandArgs())

trainingFilePath <- commandArgs()[numArgs-4]
testFilePath <- commandArgs()[numArgs-3]
classOptions <- strsplit(commandArgs()[numArgs-2], ",")[[1]]
numCores <- as.integer(commandArgs()[numArgs-1])
algorithm <- commandArgs()[numArgs]

suppressPackageStartupMessages(suppressWarnings(library(mlr)))
suppressPackageStartupMessages(library(methods))
suppressPackageStartupMessages(library(data.table))

if (numCores > 1)
{
  suppressPackageStartupMessages(suppressWarnings(library(parallelMap)))
  parallelStartSocket(2)
}

trainingData <- fread(trainingFilePath, sep="\t", stringsAsFactors = TRUE, header=TRUE, data.table=FALSE)
testData <- fread(testFilePath, sep="\t", stringsAsFactors = TRUE, header=TRUE, data.table=FALSE)

trainingData <- trainingData[,-1,drop=FALSE]
testData <- testData[,-1,drop=FALSE]

trainingColumnNames <- colnames(trainingData)
trainingClassIndex <- which(trainingColumnNames=="Class")
trainingColumnNames <- paste("Column", 1:ncol(trainingData), sep="")
trainingColumnNames[trainingClassIndex] <- "Class"
colnames(trainingData) <- trainingColumnNames

colnames(testData) <- paste("Column", 1:ncol(testData), sep="")

# The xgboost algorithm cannot deal with integer columns, so we convert these to numerics
trainingData <- as.data.frame(lapply(trainingData, function(x) {
                                                   if (is.integer(x))
                                                     return (as.numeric(x))
                                                   return (x)
                                                 }
))

testData <- as.data.frame(lapply(testData, function(x) {
                                                   if (is.integer(x))
                                                     return (as.numeric(x))
                                                   return (x)
                                                 }
))

isGlmNet <- grepl("classif\\.glmnet", algorithm)

if (isGlmNet & ncol(testData) == 1)
{
  # The glmnet algorithm has a bug where it fails if there is only one column of data.
  # So this is a workaround for that bug...
  trainingData <- cbind(rep(0, nrow(trainingData)), trainingData)
  testData <- cbind(rep(0, nrow(testData)), testData)

  colnames(trainingData)[1] <- "Zeroes"
  colnames(testData)[1] <- "Zeroes"
}

task <- makeClassifTask(data = trainingData, target = "Class")

learn <- function(learner)
{
  #set.seed(0)
  set.seed(123, "L'Ecuyer")
  mod <- suppressWarnings(train(learner, task))

  task.pred <- suppressWarnings(predict(mod, newdata = testData))
  #classtypes <- as.vector(task.pred$task.desc$class.levels)

  p1 <- suppressWarnings(getPredictionProbabilities(task.pred, classOptions))
  p2 <- as.data.frame(getPredictionResponse(task.pred))

  output <- cbind(p2, p1)

  write.table(output, "", sep="\t", row.names = FALSE, col.names=FALSE, quote = FALSE)
}

# Dynamically invoke the algorithm
instantiation <- paste("learner <- makeLearner(", algorithm ,", predict.type = 'prob')", sep="")
#print(instantiation)
learner <- eval(parse(text = instantiation))
#learner <- makeLearner(paste("classif.", algorithm, sep=""), predict.type = "prob")

#configureMlr(show.info=FALSE, on.learner.error="quiet", on.learner.warning="quiet", show.learner.output=FALSE)
configureMlr(show.learner.output=FALSE)
learn(learner)

#if (parameterDescription == "default") {
#} else {
#  parameterData <- read.table(parametersFilePath, sep="\t", header=TRUE, stringsAsFactor=F, row.names=NULL, check.names=FALSE, quote="")
#  parameterNames <- colnames(parameterData)
#
#  for (i in 1:nrow(parameterData))
#  {
#    parameterList <- list()
#
#    for (j in 1:ncol(parameterData))
#      parameterList[[parameterNames[j]]] <- parameterData[i,j]
#
#    parameterDescription <- paste(parameterNames, parameterData[i,], sep="=")
#    learner <- makeLearner(algorithm, predict.type = "prob", par.vals=parameterList)
#    learn(learner, parameterDescription)
#  }
#}

if (numCores > 1)
  parallelStop()
