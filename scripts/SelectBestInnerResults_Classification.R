inFilePath = commandArgs()[7]
trainTestFilePath = commandArgs()[8]
outCLFilePath = commandArgs()[9]

library(dplyr)

data <- read.table(inFilePath, sep="\t", header=TRUE, row.names=NULL, quote="\"", check.names=F)

data <- filter(data, Metric=="AUROC")
data <- select(data, -Metric)

# Average across the inner iterations
data <- ungroup(summarise(group_by(data, Description, CL), Value=mean(Value)))

# Pick best result for each description
groupedData <- group_by(data, Description)
set.seed(0)
groupedData <- filter(groupedData, rank(-Value, ties.method="random")==1)

trainTestData <- read.table(trainTestFilePath, sep="\t", header=FALSE, row.names=NULL, quote="\"", check.names=F)
colnames(trainTestData) <- c("Description", "TrainIDs", "TestIDs")

mergedData <- inner_join(groupedData, trainTestData)

mergedData$Description <- paste(mergedData$Description, "____Select_Best", sep="")

outCLData <- select(mergedData, Description, TrainIDs, TestIDs, CL)
write.table(outCLData, outCLFilePath, sep="\t", col.names=F, row.names=F, quote=F)
