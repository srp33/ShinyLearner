inFilePath = commandArgs()[7]
trainTestFilePath = commandArgs()[8]
outCLFilePath = commandArgs()[9]

suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(data.table))

#data <- read.table(inFilePath, sep="\t", header=TRUE, row.names=NULL, quote="\"", check.names=F)
suppressWarnings(data <- fread(inFilePath, stringsAsFactors=TRUE, sep="\t", header=TRUE, data.table=FALSE, check.names=FALSE, showProgress=FALSE))

data <- filter(data, Metric=="AUROC")
data <- select(data, -Metric)

# Average across the inner iterations
data <- ungroup(summarise(group_by(data, Description, CL), Value=mean(Value)))

# Truncate parameter combos to directory names
data$CL_Dir <- factor(dirname(as.character(data$CL)))

# Pick best result for each description
groupedData <- group_by(data, Description, CL_Dir)
set.seed(0)
groupedData <- filter(groupedData, rank(-Value, ties.method="random")==1) %>% ungroup() %>% select(-Value)

#trainTestData <- read.table(trainTestFilePath, sep="\t", header=FALSE, row.names=NULL, quote="\"", check.names=F)
suppressWarnings(trainTestData <- fread(trainTestFilePath, stringsAsFactors=TRUE, sep="\t", header=FALSE, data.table=FALSE, check.names=FALSE, showProgress=FALSE))

colnames(trainTestData) <- c("Description", "TrainIDs", "TestIDs")

mergedData <- inner_join(groupedData, trainTestData, by="Description")

mergedData$Description <- paste(mergedData$Description, "____", mergedData$CL_Dir, sep="")
#mergedData$Description <- paste(mergedData$Description, "____Ensemble_Select_Best", sep="")

mergedData <- select(mergedData, Description, TrainIDs, TestIDs, CL)

write.table(mergedData, outCLFilePath, sep="\t", col.names=F, row.names=F, quote=F)
