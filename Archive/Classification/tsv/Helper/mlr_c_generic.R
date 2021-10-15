trainingFilePath <- commandArgs()[7]
testFilePath <- commandArgs()[8]
classOptions <- strsplit(commandArgs()[9], ",")[[1]]
algorithm <- commandArgs()[10]

suppressPackageStartupMessages(library(mlr))
suppressPackageStartupMessages(library(methods))

trainingData <- read.table(trainingFilePath, sep="\t", stringsAsFactors = TRUE, header=TRUE, row.names = 1, check.names=FALSE, quote=NULL)
testData <- read.table(testFilePath, sep="\t", stringsAsFactors = TRUE, header=TRUE, row.names = 1, check.names=FALSE, quote=NULL)

task.lrn = makeClassifTask(data = trainingData, target = "Class")
lrn = makeLearner(algorithm, predict.type = "prob")
set.seed(0)
mod = train(lrn, task.lrn)

task.pred = predict(mod, newdata = testData)
#classtypes <- as.vector(task.pred$task.desc$class.levels)

p1 <- getPredictionProbabilities(task.pred, classOptions)
p2 <- as.data.frame(getPredictionResponse(task.pred))
colnames(p2) <- "Prediction"

output <- cbind(p2, p1)

write.table(output, "", sep="\t", row.names = FALSE, col.names=FALSE, quote = FALSE)
