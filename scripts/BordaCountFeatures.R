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

  result <- data.frame(Features=uniqueFeatures, MeanRanks=meanRank)
  return(result[order(meanRank),])
}

#Description	Iteration	AlgorithmScript	Features
#Description	Iteration	Fold	AlgorithmScript	Features
#Description	Iteration	Ensemble_Algorithm	AlgorithmScript	Features
#Description	Iteration	Fold	Ensemble_Algorithm	AlgorithmScript	Features
data <- read_tsv(inFilePath)

#groupRankMatrix <- NULL
#for (algorithmScript in unique(data$AlgorithmScript))
#{
#  algorithmData <- filter(data, AlgorithmScript==algorithmScript)
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
