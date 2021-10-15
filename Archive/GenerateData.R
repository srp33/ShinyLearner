generate = function(numContinuousRandom, numContinuousSignal, numDiscreteRandom, numDiscreteSignal, numInstances, outFilePrefix, group2Mean=0)
{
  numContinuous = numContinuousRandom + numContinuousSignal
  numDiscrete = numDiscreteRandom + numDiscreteSignal

  outDataFilePath = paste(outFilePrefix, ".tsv.gz", sep="")

  set.seed(0)

  dataMatrix = NULL

  if (numContinuous > 0)
  {
    dataMatrix1 = matrix(rnorm(numInstances / 2 * numContinuous, mean=0), nrow=numInstances / 2, ncol=numContinuous)
    dataMatrix21 = matrix(rnorm(numInstances / 4 * numContinuousSignal, mean=group2Mean), nrow=numInstances / 4, ncol=numContinuousSignal)
    dataMatrix22 = matrix(rnorm(numInstances / 4 * numContinuousRandom, mean=0), nrow=numInstances / 4, ncol=numContinuousRandom)
    dataMatrix31 = matrix(rnorm(numInstances / 4 * numContinuousSignal, mean=-group2Mean), nrow=numInstances / 4, ncol=numContinuousSignal)
    dataMatrix32 = matrix(rnorm(numInstances / 4 * numContinuousRandom, mean=0), nrow=numInstances / 4, ncol=numContinuousRandom)

    dataMatrix = rbind(dataMatrix1, cbind(dataMatrix21, dataMatrix22))
    dataMatrix = rbind(dataMatrix, cbind(dataMatrix31, dataMatrix32))
  }

  if (numDiscrete > 0)
  {
    values1 = sample(c(rep(-1, numInstances / 6 * numDiscrete), rep(0, numInstances / 6 * numDiscrete), rep(1, numInstances / 6 * numDiscrete)))

    if (group2Mean == 0)
      values21 = sample(c(rep(-1, numInstances / 12 * numDiscrete), rep(0, numInstances / 12 * numDiscrete), rep(1, numInstances / 12 * numDiscrete)))
    if (group2Mean == 1)
      values21 = c(rep(-1, numInstances / 12 * numDiscrete), rep(0, numInstances / 12 * numDiscrete), rep(1, numInstances / 12 * numDiscrete))
    if (group2Mean == 5)
      values21 = c(rep(-1, numInstances / 12 * numDiscrete), rep(0, numInstances / 12 * numDiscrete), rep(1, numInstances / 12 * numDiscrete))

    values22 = sample(c(rep(-1, numInstances / 12 * numDiscrete), rep(0, numInstances / 12 * numDiscrete), rep(1, numInstances / 12 * numDiscrete)))

    dataMatrix1 = matrix(paste("Value", values1, sep=""), nrow=numInstances / 2, ncol=numDiscrete)
    dataMatrix21 = matrix(paste("Value", values21, sep=""), nrow=numInstances / 2, ncol=numDiscreteSignal)
    dataMatrix22 = matrix(paste("Value", values22, sep=""), nrow=numInstances / 2, ncol=numDiscreteRandom)
    dataMatrix2 = cbind(dataMatrix21, dataMatrix22)
    dataMatrixDiscrete = rbind(dataMatrix1, cbind(dataMatrix21, dataMatrix22))

    dataMatrix = cbind(dataMatrix, dataMatrixDiscrete)
  }

stop("got here")
  data = as.data.frame(dataMatrix)
  colnames(data) = paste("Feature", 1:ncol(data), sep="")
  rownames(data) = paste("Instance", 1:nrow(data), sep="")

  classValues = c(rep(1, numInstances / 2), rep(2, numInstances / 4), rep(3, numInstances / 4))

  classData = as.data.frame(matrix(classValues, ncol=1))
  colnames(classData) = "Class"

  data <- cbind(data, classData)

  outDataFile = gzfile(outDataFilePath, "w")

  write.table(data, outDataFile, sep="\t", row.names=T, col.names=NA, quote=F)

  close(outDataFile)
}

#generate(95, 5, 0, 0, 60, "NoSignal_Continuous", 0)
#generate(95, 5, 0, 0, 60, "MediumSignal_Continuous", 1)
#generate(95, 5, 0, 0, 60, "StrongSignal_Continuous", 5)

#generate(0, 0, 95, 5, 60, "NoSignal_Discrete", 0)
#generate(0, 0, 95, 5, 60, "MediumSignal_Discrete", 1)
generate(0, 0, 95, 5, 60, "StrongSignal_Discrete", 5)

#generate(45, 5, 45, 5, 60, "NoSignal_Both", 0)
#generate(45, 5, 45, 5, 60, "MediumSignal_Both", 1)
#generate(45, 5, 45, 5, 60, "StrongSignal_Both", 5)
