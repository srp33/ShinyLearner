suppressPackageStartupMessages(library(readr))
suppressPackageStartupMessages(library(dplyr))

inFilePath <- commandArgs()[7]
outFilePath <- commandArgs()[8]

calculateMajority <- function(data, classOptions)
{
  tbl <- table(data$PredictedClass)
  classesMatchingMax <- names(tbl)[which(tbl==max(tbl))]

  set.seed(0)
  majorityVote <- sample(classesMatchingMax, size=1)

  data2 <- data
  data2$AlgorithmScript <- rep("Majority Vote", nrow(data2))

  data2 <- unique(select(data2, Description, AlgorithmScript, InstanceID, ActualClass))

  data2$PredictedClass <- majorityVote

  totalPredictions <- sum(tbl)

  for (classOption in classOptions)
  {
    numVotes <- sum(data2$PredictedClass == classOption)
    classPrediction <- numVotes / totalPredictions
    data2 <- cbind(data2, classPrediction)
  }

  colnames(data2)[(ncol(data) - length(classOptions) + 1):ncol(data)] <- classOptions

  return(data2)
}

#Description	AlgorithmScript	InstanceID	ActualClass	PredictedClass	1	2	3
data <- read.table(inFilePath, stringsAsFactors=TRUE, sep="\t", header=TRUE, row.names=NULL, check.names=FALSE)

if (length(unique(data$AlgorithmScript)) > 1)
{
  classOptions <- colnames(data)[(which(colnames(data)=="PredictedClass") + 1):ncol(data)]

  majorityVoteData <- do(group_by(data, Description, InstanceID), calculateMajority(., classOptions))

  data <- rbind(data, as.data.frame(majorityVoteData))
}

write_tsv(data, outFilePath)
