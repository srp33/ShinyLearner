library(mlr)

inFilePath <- commandArgs()[7]
outFilePath <- commandArgs()[8]

data <- read.table(inFilePath, sep="\t", header=T, row.names=1, check.names=F)

#numFeatures <- ncol(data) - 1

data2 <- createDummyFeatures(data, target = "Class", method = "reference")
rownames(data2) <- rownames(data)

for (i in 1:ncol(data2))
{
  colName <- colnames(data2)[i]

  if (colName %in% colnames(data))
    next

  dataType <- class(data2[,i])
  if (dataType == "factor")
  {
    numUniq <- length(unique(data[,colName]))
    if (numUniq == 2)
    {
      newColName <- colnames(data2)[i]
      newColName <- strsplit(newColName, "\\.")[[1]][1]
      colnames(data2)[i] <- newColName
    }
  }
}

write.table(data2, outFilePath, sep="\t", row.names=T, col.names=NA, quote=F)
