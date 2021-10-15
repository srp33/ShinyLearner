library(mlr)

inFilePath <- commandArgs()[7]
outFilePath <- commandArgs()[8]

data <- read.table(inFilePath, sep="\t", header=T, row.names=1, check.names=F)

data2 <- impute(data, target="Class", classes = list(numeric = imputeMedian(), integer = imputeMedian(), factor = imputeMode()))
data2 <- data2$data
rownames(data2) <- rownames(data)

write.table(data2, outFilePath, sep="\t", row.names=T, col.names=NA, quote=F)
