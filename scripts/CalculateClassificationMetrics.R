suppressPackageStartupMessages(suppressWarnings(library(mlr)))
suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(data.table))
suppressPackageStartupMessages(library(AUC))

inPredictionsFilePath <- commandArgs()[7]
outMetricsFilePath <- commandArgs()[8]

calculateMetrics <- function(predictionData)
{
  levels <- sort(unique(c(as.character(predictionData$ActualClass), as.character(predictionData$PredictedClass))))
  truth <- factor(predictionData$ActualClass, levels=levels)
  response <- factor(predictionData$PredictedClass, levels=levels)
  probabilities <- predictionData$Probabilities

  accuracy <- measureACC(truth, response)
  #auc <- ROCR::performance(ROCR::prediction(probabilities, truth, label.ordering=c(0, 1)), "auc")@y.values[[1L]]
  auc <- auc(roc(probabilities, truth))
  #balancedAccuracy <- measureBAC(truth, response, 0, 1)
  balancedAccuracy <- measureBAC(truth, response)
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

  #logLoss <- measureLogloss(probabilities, truth)
  #ssr <- measureSSR(probabilities, truth)
  #multiHamLoss <- measureMultilabelHamloss(truth, response)

  list(Accuracy=accuracy, AUROC=auc, BalancedAccuracy=balancedAccuracy, Brier=brier, FDR=fdr, FNR=fnr, FPR=fpr, MCC=mcc, MMCE=mmce, PPV=ppv, NPV=npv, TNR=tnr, TPR=tpr, Recall=recall, F1=f1)
}

#Description	Algorithm	InstanceID	ActualClass	PredictedClass	0	1
#predictionsData <- read.table(inPredictionsFilePath, sep="\t", header=TRUE, row.names=NULL, quote="\"", check.names=FALSE)
suppressWarnings(predictionsData <- fread(inPredictionsFilePath, stringsAsFactors=TRUE, sep="\t", header=TRUE, data.table=FALSE, check.names=FALSE, showProgress=FALSE))

if ("ERROR" %in% predictionsData$PredictedClass) {
  cat("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
  cat("Error: Algorithm performance could not be calculated because at least one algorithm experienced an error. To troubleshoot the error, reexecute ShinyLearner in verbose mode.\n")
  cat("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
  stop()
} else {
  predictionStartIndex <- which(colnames(predictionsData) == "PredictedClass") + 1
  classOptions <- colnames(predictionsData)[predictionStartIndex:ncol(predictionsData)]

  # The Description column is a concatenation of multiple values (e.g, description, iteration, num features).
  #   This is different depending on what type of analysis we are doing. But we since they are all
  #   combined, we can aggregate the results consistently based on that column.
  uniqueCombinations <- distinct(select(predictionsData, Description, Algorithm))

  outDescriptions <- NULL
  outAlgorithms <- NULL
  outMetrics <- NULL
  outValues <- NULL

  for (i in 1:nrow(uniqueCombinations))
  {
    description <- as.character(uniqueCombinations[i,"Description"])
    algorithm <- as.character(uniqueCombinations[i,"Algorithm"])

    combinationPredictionData <- filter(predictionsData, Description==description & Algorithm==algorithm)

    if (length(classOptions) == 2) {
      classOptions <- classOptions[1]
    }

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
        outAlgorithms <- c(outAlgorithms, algorithm)
        outMetrics <- c(outMetrics, metric)
        outValues <- c(outValues, metrics[[metric]])
      }
    }
  }

  outData <- data.frame(Description=outDescriptions, Algorithm=outAlgorithms, Metric=outMetrics, Value=outValues)
  outData <- as.data.frame(ungroup(summarize(group_by(outData, Description, Algorithm, Metric), Value=mean(Value))))

  write.table(outData, outMetricsFilePath, sep="\t", col.names=TRUE, row.names=FALSE, quote=FALSE)
}
