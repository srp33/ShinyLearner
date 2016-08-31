library(mlr)
library(dplyr)
library(AUC)

inPredictionsFilePath <- commandArgs()[7]
outMetricsFilePath <- commandArgs()[8]

calculateMetrics <- function(predictionData)
{
  levels <- sort(unique(c(predictionData$ActualClass, predictionData$PredictedClass)))
  truth <- factor(predictionData$ActualClass, levels=levels)
  response <- factor(predictionData$PredictedClass, levels=levels)
  probabilities <- predictionData$Probabilities

  accuracy <- measureACC(truth, response)
  #auc <- ROCR::performance(ROCR::prediction(probabilities, truth, label.ordering=c(0, 1)), "auc")@y.values[[1L]]
  auc <- auc(roc(probabilities, truth))
  balancedAccuracy <- measureBAC(truth, response, 0, 1)
  brier <- measureBrier(probabilities, truth, 0, 1)
  fdr <- measureFDR(truth, response, 1)
  fn <- measureFN(truth, response, 0)
  fnr <- measureFNR(truth, response, 0, 1)
  fp <- measureFP(truth, response, 1)
  fpr <- measureFPR(truth, response, 0, 1)
  #gmean <- measureGMEAN(truth, response, 0, 1)
  #gpr <- measureGPR(truth, response, 1)
  mcc <- measureMCC(truth, response, 0, 1)
  mmce <- measureMMCE(truth, response)
  ppv <- measurePPV(truth, response, 1)
  npv <- measureNPV(truth, response, 0)
  tn <- measureTN(truth, response, 1)
  tnr <- measureTNR(truth, response, 0)
  tp <- measureTP(truth, response, 1)
  tpr <- measureTPR(truth, response, 1)

  precision <- tp / (tp + fp)
  recall <- tp / (tp + fn)
  f1 <- (2 * precision * recall) / sum(precision, recall)

  list(Accuracy=accuracy, AUROC=auc, BalancedAccuracy=balancedAccuracy, Brier=brier, FDR=fdr, FNR=fnr, FPR=fpr, MCC=mcc, MMCE=mmce, PPV=ppv, NPV=npv, TNR=tnr, TPR=tpr, Precision=precision, Recall=recall, F1=f1)
}

#Description	AlgorithmScript	InstanceID	ActualClass	PredictedClass	0	1
predictionsData <- read.table(inPredictionsFilePath, sep="\t", header=TRUE, row.names=NULL, quote="\"", check.names=FALSE)

predictionStartIndex <- which(colnames(predictionsData) == "PredictedClass") + 1
classOptions <- colnames(predictionsData)[predictionStartIndex:ncol(predictionsData)]

uniqueCombinations <- distinct(select(predictionsData, Description, AlgorithmScript))

outDescriptions <- NULL
outAlgorithmScripts <- NULL
outMetrics <- NULL
outValues <- NULL

for (i in 1:nrow(uniqueCombinations))
{
  description <- as.character(uniqueCombinations[i,"Description"])
  algorithmScript <- as.character(uniqueCombinations[i,"AlgorithmScript"])

  combinationPredictionData <- filter(predictionsData, Description==description & AlgorithmScript==algorithmScript)

  if (length(classOptions) == 2) {
    combinationPredictionData$Probabilities <- combinationPredictionData[,"1"]
    metrics <- calculateMetrics(combinationPredictionData)

    for (metric in names(metrics))
    {
      outDescriptions <- c(outDescriptions, description)
      outAlgorithmScripts <- c(outAlgorithmScripts, algorithmScript)
      outMetrics <- c(outMetrics, metric)
      outValues <- c(outValues, metrics[[metric]])
    }
  } else {
    for (classOption in classOptions)
    {
      tmpPred <- combinationPredictionData

      actual <- as.character(tmpPred$ActualClass)
      actual[tmpPred$ActualClass==classOption] <- 1
      actual[tmpPred$ActualClass!=classOption] <- 0
      tmpPred$ActualClass <- actual

      predicted <- as.character(tmpPred$PredictedClass)
      predicted[tmpPred$PredictedClass==classOption] <- 1
      predicted[tmpPred$PredictedClass!=classOption] <- 0
      tmpPred$PredictedClass <- predicted

      colnames(tmpPred)[which(colnames(tmpPred)==classOption)] <- "Probabilities"

      metrics <- calculateMetrics(tmpPred)

      for (metric in names(metrics))
      {
        outDescriptions <- c(outDescriptions, description)
        outAlgorithmScripts <- c(outAlgorithmScripts, algorithmScript)
        outMetrics <- c(outMetrics, metric)
        outValues <- c(outValues, metrics[[metric]])
      }
    }
  }
}

outData <- data.frame(Description=outDescriptions, AlgorithmScript=outAlgorithmScripts, Metric=outMetrics, Value=outValues)
outData <- as.data.frame(ungroup(summarize(group_by(outData, Description, AlgorithmScript, Metric), Value=mean(Value))))

write.table(outData, outMetricsFilePath, sep="\t", col.names=TRUE, row.names=FALSE, quote=FALSE)
