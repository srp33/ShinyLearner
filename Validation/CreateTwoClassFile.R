library(readr)
library(dplyr)

inFilePath <- commandArgs()[7]
outFilePath <- commandArgs()[8]

data <- suppressWarnings(read_tsv(inFilePath))

data <- filter(data, Class %in% c(1, 2))

colnames(data)[1] <- ""

write_tsv(data, outFilePath)
