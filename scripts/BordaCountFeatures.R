suppressPackageStartupMessages(library(readr))
suppressPackageStartupMessages(library(dplyr))

inFilePath <- commandArgs()[7]
outFilePath <- commandArgs()[8]
numTop <- commandArgs()[9]

buildRankMatrix <- function(dataSubset)
{
  featuresMatrix <- t(data.frame(lapply(dataSubset$Features, function(x) {strsplit(x,',')})))
  rownames(featuresMatrix) <- NULL

  return(featuresMatrix)
}

rankAggregate <- function(featuresMatrix)
{
  uniqueFeatures <- unique(as.vector(featuresMatrix))
  rankMatrix <- NULL

  for (i in 1:nrow(featuresMatrix))
  {
    rowFeatures <- featuresMatrix[i,]
    rowRanks <- match(uniqueFeatures, rowFeatures)
    rankMatrix <- cbind(rankMatrix, rowRanks)
  }

  meanRank <- apply(rankMatrix, 1, mean)

  result <- data.frame(Feature=uniqueFeatures, Mean_Rank=meanRank)
  return(result[order(meanRank),])
}

#Description	Iteration	Algorithm	Features
#Description	Iteration	Fold	Algorithm	Features
#Description	Iteration	Ensemble_Algorithm	Algorithm	Features
#Description	Iteration	Fold	Ensemble_Algorithm	Algorithm	Features
data <- suppressMessages(read_tsv(inFilePath))

if ("ERROR" %in% data$Features)
{
  cat("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
  cat("Error: Feature ranks could not be summarized because at least one individual algorithm experienced an error. To troubleshoot the error, reexecute ShinyLearner in verbose mode.\n")
  cat("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
  stop()
}

#groupRankMatrix <- NULL
#for (algorithm in unique(data$Algorithm))
#{
#  algorithmData <- filter(data, Algorithm==algorithm)
#  algorithmRanks <- rankAggregate(buildRankMatrix(algorithmData))
#  groupRankMatrix <- rbind(groupRankMatrix, as.character(algorithmRanks$Features))
#}

#overallRanks <- rankAggregate(groupRankMatrix)

overallRanks <- rankAggregate(buildRankMatrix(data))

if (!is.na(numTop))
{
  numTop <- min(c(as.integer(numTop), nrow(overallRanks)))
  overallRanks <- overallRanks[1:numTop,]
}

write_tsv(overallRanks, outFilePath)
