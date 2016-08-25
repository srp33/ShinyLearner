inFilePath <- commandArgs()[7]
outFilePath <- commandArgs()[8]

data <- read.table(inFilePath, sep="\t", header=T, row.names=1, check.names=F)

for (i in 1:ncol(data))
{
  colName <- colnames(data)[i]
  if (colName == "Class")
    next

  dataType <- class(data[,i])
  if (dataType != "numeric")
    next

  data[,i] <- scale(data[,i])
}

write.table(data, outFilePath, sep="\t", row.names=T, col.names=NA, quote=F)
