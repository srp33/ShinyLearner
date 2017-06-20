library(mlr)

inFilePath <- commandArgs()[7]
outFilePath <- commandArgs()[8]

data <- read.table(inFilePath, sep="\t", header=T, row.names=1, check.names=F)

addToDataFrame <- function(currentData, newData)
{
  if (is.null(currentData)) {
    return(as.data.frame(newData))
  } else {
    return(cbind(currentData, newData))
  }
}

data2 <- NULL

for (colName in colnames(data))
{
  dataType <- class(data[,colName])
  isFactor <- dataType == "factor"

  if (isFactor) {
    dataTmp <- createDummyFeatures(data[,c(colName, "Class")], target = "Class", method = "reference")
    dataTmp <- dataTmp[,-which(colnames(dataTmp)=="Class"),drop=FALSE]

    if (nlevels(data[,colName]) == 2)
      colnames(dataTmp) <- colName

    data2 <- addToDataFrame(data2, dataTmp)
  } else {
    data2 <- addToDataFrame(data2, data[,colName,drop=FALSE])
  }
}

write.table(data2, outFilePath, sep="\t", row.names=T, col.names=NA, quote=F)
