inFilePath = commandArgs()[7]
trainTestFilePath = commandArgs()[8]
outCLFilePath = commandArgs()[9]

suppressPackageStartupMessages(library(dplyr))

data <- read.table(inFilePath, sep="\t", header=TRUE, row.names=NULL, quote="\"", check.names=F)

data <- filter(data, Metric=="AUROC")
data <- select(data, -Metric)

###
write.table(arrange(data, CL), "/Users/srp33/Downloads/aa.txt", sep="\t", quote=F, col.names=T, row.names=F)

# Average across the inner iterations
data <- ungroup(summarise(group_by(data, Description, CL), Value=mean(Value)))

# Truncate parameter combos to directory names
data$CL_Dir <- factor(dirname(as.character(data$CL)))

###
write.table(arrange(data, CL), "/Users/srp33/Downloads/bb.txt", sep="\t", quote=F, col.names=T, row.names=F)

# Pick best result for each description
groupedData <- group_by(data, Description, CL_Dir)
set.seed(0)
###groupedData <- filter(groupedData, rank(-Value, ties.method="random")==1) %>% ungroup() %>% select(-Value, -CL_Dir)
groupedData <- filter(groupedData, rank(-Value, ties.method="random")==1) %>% ungroup() %>% select(-CL_Dir)

###
write.table(arrange(groupedData, CL), "/Users/srp33/Downloads/cc.txt", sep="\t", quote=F, col.names=T, row.names=F)

trainTestData <- read.table(trainTestFilePath, sep="\t", header=FALSE, row.names=NULL, quote="\"", check.names=F)
colnames(trainTestData) <- c("Description", "TrainIDs", "TestIDs")

mergedData <- inner_join(groupedData, trainTestData, by="Description")

mergedData$Description <- paste(mergedData$Description, "____Ensemble_Select_Best", sep="")

outCLData <- select(mergedData, Description, TrainIDs, TestIDs, CL)
write.table(outCLData, outCLFilePath, sep="\t", col.names=F, row.names=F, quote=F)
