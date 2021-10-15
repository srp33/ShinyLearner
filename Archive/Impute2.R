suppressPackageStartupMessages(library(readr))
suppressPackageStartupMessages(library(dplyr))

inFilePath = commandArgs()[7]
verbose = commandArgs()[8] == "true"

suppressMessages(suppressWarnings(data <- read_tsv(inFilePath, progress=FALSE) %>% mutate_if(is.character, factor) %>% as.data.frame))

rownames(data) <- data[,1]
data <- data[,-1]

classColIndex <- which(colnames(data) == "Class")
Class <- data[,classColIndex]
data <- data[,-classColIndex]

saveData <- FALSE

proportionMissingPerFeature <- apply(data, 2, function(x) {sum(sapply(x, is.na)) / length(x)})

if (any(proportionMissingPerFeature > 0.5))
{
  print(paste("More than 50% of instances were missing data for ", sum(proportionMissingPerFeature > 0.5), " features, which exceeds the threshold for imputation. These features were removed.", sep=""))

  data <- data[, which(proportionMissingPerFeature > 0.5)]
  saveData <- TRUE
}

proportionMissingPerSample <- apply(data, 1, function(x) {sum(sapply(x, is.na)) / length(x)})

if (any(proportionMissingPerSample > 0.5))
{
  print(paste("More than 50% of data values were missing for ", sum(proportionMissingPerSample > 0.5), " instances, which exceeds the threshold for imputation. These instances were removed.", sep=""))

  data <- data[which(proportionMissingPerSample > 0.5),]
  saveData <- TRUE
}

proportionMissingPerSample <- apply(data, 1, function(x) {sum(sapply(x, is.na)) / length(x)})

if (any(proportionMissingPerSample > 0))
{
  suppressPackageStartupMessages(library(mlr))

  if (verbose)
    print("Performing imputation")

  rNames <- rownames(data)
  print(tail(data))
  data <- impute(data, classes = list(numeric = imputeMedian(), integer = imputeMedian(), factor = imputeMode()), impute.new.levels=FALSE)$data
  rownames(data) <- rNames

  saveData <- TRUE
}

if (saveData)
{
  data <- cbind(rownames(data), data)
  data <- cbind(data, Class)
  colnames(data)[1] <- ""

  if (verbose)
    print(paste("Saving imputed data to ", inFilePath, sep=""))

  suppressWarnings(write_tsv(data, inFilePath))
}
