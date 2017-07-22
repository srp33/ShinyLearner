suppressPackageStartupMessages(library(RankAggreg))
suppressPackageStartupMessages(library(data.table))

inFilePath <- commandArgs()[7]
numTop <- as.integer(commandArgs()[8])
outFilePath <- commandArgs()[9]

#Description	Iteration	Fold	Ensemble_Algorithm	Algorithm	Features
#data <- read.table(inFilePath, sep="\t", header=TRUE, row.names=NULL, check.names=FALSE, stringsAsFactors=FALSE)
suppressWarnings(data <- fread(inFilePath, stringsAsFactors=TRUE, sep="\t", header=TRUE, data.table=FALSE, check.names=FALSE, showProgress=FALSE))
data <- data[,c("Iteration","Fold","Features")]

splitFeatures <- t(data.frame(lapply(data$Features, function(x) {strsplit(x,',')})))
rownames(splitFeatures) <- NULL

# The CE method is very slow
#f_agg <- RankAggreg(splitFeatures, numTop, seed=0, method="CE", maxIter=10, verbose=TRUE)
f_agg <- RankAggreg(splitFeatures, numTop, seed=0, method="GA", maxIter=1000, verbose=FALSE)
f_agg = data.frame(f_agg$top.list)
