inFilePath <- commandArgs()[7]
outFilePath <- commandArgs()[8]

data <- read.table(inFilePath, header=FALSE, row.names=NULL)$V1

data <- data[which(data!=0)]

pdf(outFilePath)
plot(1:length(data), data, xlab="Time", ylab="Memory", type="b", pch=20)
graphics.off()
