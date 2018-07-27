suppressPackageStartupMessages(library(readr))
suppressPackageStartupMessages(library(dplyr))

inFilePath = commandArgs()[7]
verbose = commandArgs()[8] == "true"

hasOnlyIntegers <- function(x)
{
  return(all(sapply(x, function(z) { is.na(z) | z%%1 == 0 })))
}

suppressWarnings(suppressMessages(data <- read_tsv(inFilePath, progress=FALSE) %>% mutate_if(is.character, factor) %>% as.data.frame))
rownames(data) <- data[,1]
data <- data[,-1]

numScaled <- 0

for (colName in colnames(data))
{
  if (colName == "Class")
  {
    if (verbose)
      print("Skipping the Class column when standardizing.")

    next
  }

  if (!is.numeric(data[,colName]))
  {
    if (verbose)
      print(paste("The ", colName, " column is not numeric, so it will not be scaled.", sep=""))

    next
  }

  if (hasOnlyIntegers(data[,colName]) & length(unique(data[,colName])) < nrow(data) * 0.5)
  {
    if (verbose)
      print(paste("The ", colName, " column contains integers but fewer than half are distinct values, so it will not be scaled.", sep=""))

    next
  }

  if (length(unique(data[,colName])) == 1)
  {
    print(data[,colName])
    if (verbose)
      print(paste("The ", colName, " column has only one distinct value across all samples, so it will not be scaled.", sep=""))

    next
  }

  if (verbose)
    print(paste("Scaling values for column ", colName, sep=""))

  data[,colName] <- scale(data[,colName])
  numScaled <- numScaled + 1
}

if (numScaled > 0)
{
  if (verbose)
    print(paste("Saving scaled version of data to ", inFilePath, sep=""))

  data <- cbind(rownames(data), data)
  colnames(data)[1] <- ""
  suppressWarnings(write_tsv(data, inFilePath))
}
