numArgs <- length(commandArgs())

trainingFilePath <- commandArgs()[numArgs-3]
testFilePath <- commandArgs()[numArgs-2]
classOptions <- strsplit(commandArgs()[numArgs-1], ",")[[1]]
algorithm <- commandArgs()[numArgs]

suppressPackageStartupMessages(library(mlr))
suppressPackageStartupMessages(library(methods))
suppressPackageStartupMessages(library(data.table))

trainingData <- fread(trainingFilePath, sep="\t", stringsAsFactors = TRUE, header=TRUE, data.table=FALSE)
testData <- fread(testFilePath, sep="\t", stringsAsFactors = TRUE, header=TRUE, data.table=FALSE)

trainingData <- trainingData[,-1]
testData <- testData[,-1]

task <- makeClassifTask(data = trainingData, target = "Class")

learn <- function(learner)
{
  #set.seed(0)
  set.seed(123, "L'Ecuyer")
  mod <- train(learner, task)

  task.pred <- predict(mod, newdata = testData)
  #classtypes <- as.vector(task.pred$task.desc$class.levels)

  p1 <- getPredictionProbabilities(task.pred, classOptions)
  p2 <- as.data.frame(getPredictionResponse(task.pred))

  output <- cbind(p2, p1)

  write.table(output, "", sep="\t", row.names = FALSE, col.names=FALSE, quote = FALSE)
}

# Dynamically invoke the algorithm
instantiation <- paste("learner <- makeLearner(", algorithm ,", predict.type = 'prob')", sep="")
print(instantiation)
learner <- eval(parse(text = instantiation))
#learner <- makeLearner(paste("classif.", algorithm, sep=""), predict.type = "prob")

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
