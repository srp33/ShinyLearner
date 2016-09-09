trainingFilePath <- commandArgs()[7]
testFilePath <- commandArgs()[8]
classOptions <- strsplit(commandArgs()[9], ",")[[1]]
algorithm <- commandArgs()[10]
parameterDescription <- commandArgs()[11]

suppressPackageStartupMessages(library(mlr))
suppressPackageStartupMessages(library(methods))

trainingData <- read.table(trainingFilePath, sep="\t", stringsAsFactors = TRUE, header=TRUE, row.names = 1, check.names=FALSE, quote=NULL)
testData <- read.table(testFilePath, sep="\t", stringsAsFactors = TRUE, header=TRUE, row.names = 1, check.names=FALSE, quote=NULL)

task <- makeClassifTask(data = trainingData, target = "Class")

learn <- function(learner)
{
  set.seed(0)
  mod <- train(learner, task)

  task.pred <- predict(mod, newdata = testData)
  #classtypes <- as.vector(task.pred$task.desc$class.levels)

  p1 <- getPredictionProbabilities(task.pred, classOptions)
  p2 <- as.data.frame(getPredictionResponse(task.pred))

  output <- cbind(p2, p1)

  write.table(output, "", sep="\t", row.names = FALSE, col.names=FALSE, quote = FALSE)
}

#if (parameterDescription == "default") {
  learn(makeLearner(algorithm, predict.type = "prob"))
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
