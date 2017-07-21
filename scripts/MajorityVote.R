suppressPackageStartupMessages(library(data.table))
suppressPackageStartupMessages(library(readr))
suppressPackageStartupMessages(library(dplyr))

inFilePath <- commandArgs()[7]
outFilePath <- commandArgs()[8]

calculateMajority <- function(data, classOptions)
{
  data2 <- as.data.frame(data)

  tbl <- table(data2$PredictedClass)
  classesMatchingMax <- names(tbl)[which(tbl==max(tbl))]

  set.seed(0)
  majorityVote <- sample(classesMatchingMax, size=1)

  totalPredictions <- sum(tbl)

  classProbs <- NULL
  for (classOption in classOptions)
  {
    numVotes <- sum(data2$PredictedClass == classOption)
    classProb <- numVotes / totalPredictions
    classProbs <- c(classProbs, classProb)
  }

  description <- unique(as.character(data2$Description))
  instanceID <- unique(as.character(data2$InstanceID))
  actualClass <- unique(as.character(data2$ActualClass))

  outData <- data.frame(Description=description, Algorithm="Ensemble_Majority_Vote", InstanceID=instanceID, ActualClass=actualClass, PredictedClass=majorityVote)

  for (classProb in classProbs)
    outData <- cbind(outData, classProb)

  colnames(outData) <- c("Description", "Algorithm", "InstanceID", "ActualClass", "PredictedClass", classOptions)

  return(outData)
}

#Description	Algorithm	InstanceID	ActualClass	PredictedClass	1	2	3
suppressWarnings(data <- fread(inFilePath, stringsAsFactors=TRUE, sep="\t", header=TRUE, data.table=FALSE, check.names=FALSE, showProgress=FALSE))

if (!("ERROR" %in% data$PredictedClass)) {
  classOptions <- colnames(data)[(which(colnames(data)=="PredictedClass") + 1):ncol(data)]

  majorityVoteData <- suppressWarnings(do(group_by(data, Description, InstanceID), calculateMajority(., classOptions)))
  majorityVoteData <- as.data.frame(majorityVoteData)

  data <- rbind(data, majorityVoteData)
}

write_tsv(data, outFilePath)
