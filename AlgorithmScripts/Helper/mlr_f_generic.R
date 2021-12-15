numArgs <- length(commandArgs())

dataFilePath <- commandArgs()[numArgs - 2]
numCores <- as.integer(commandArgs()[numArgs - 1])
algorithm <- commandArgs()[numArgs]

suppressPackageStartupMessages(suppressWarnings(library(mlr)))
suppressPackageStartupMessages(library(methods))

if (numCores > 1)
{
  suppressPackageStartupMessages(suppressWarnings(library(parallelMap)))
  parallelStartSocket(2, storagedir="/tmp")
}

data <- read.table(dataFilePath, sep="\t", stringsAsFactors = TRUE, header=TRUE, row.names = 1, check.names=FALSE)

columnNames <- colnames(data)
classIndex <- which(columnNames=="Class")
modColumnNames <- paste("Column", 1:ncol(data), sep="")
modColumnNames[classIndex] <- "Class"
colnames(data) <- modColumnNames

task <- makeClassifTask(data = data, target = "Class")

set.seed(0)

# Dynamically execute the code for the specified algorithm and parameters.
code = paste0("fv = suppressWarnings(generateFilterValuesData(task, method = ", algorithm, ")$data)")
eval(parse(text = code))

fv[,1] = columnNames[-classIndex]
fv = fv[order(fv$value, decreasing=TRUE),,drop=FALSE]
fv = as.data.frame(fv[,1])

print(fv)

if (numCores > 1)
  parallelStop()
