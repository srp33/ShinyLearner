generate = function(numContinuousRandom, numContinuousSignal, numDiscreteRandom, numDiscreteSignal, numInstances, outFilePrefix, group2Mean=0)
{
  numContinuous = numContinuousRandom + numContinuousSignal
  numDiscrete = numDiscreteRandom + numDiscreteSignal

  outDataFilePath = paste(outFilePrefix, ".tsv.gz", sep="")

  set.seed(0)

  continuousMatrix = NULL

  if (numContinuous > 0)
  {
    dataMatrix1 = matrix(rnorm(numInstances / 2 * numContinuous, mean=0), nrow=numInstances / 2, ncol=numContinuous)
    dataMatrix21 = matrix(rnorm(numInstances / 4 * numContinuousSignal, mean=group2Mean), nrow=numInstances / 4, ncol=numContinuousSignal)
    dataMatrix22 = matrix(rnorm(numInstances / 4 * numContinuousRandom, mean=0), nrow=numInstances / 4, ncol=numContinuousRandom)
    dataMatrix31 = matrix(rnorm(numInstances / 4 * numContinuousSignal, mean=-group2Mean), nrow=numInstances / 4, ncol=numContinuousSignal)
    dataMatrix32 = matrix(rnorm(numInstances / 4 * numContinuousRandom, mean=0), nrow=numInstances / 4, ncol=numContinuousRandom)

    continuousMatrix = rbind(dataMatrix1, cbind(dataMatrix21, dataMatrix22))
    continuousMatrix = rbind(continuousMatrix, cbind(dataMatrix31, dataMatrix32))
  }

  discreteMatrix = NULL

  if (numDiscrete > 0)
  {
    dataMatrix1 = matrix(discretize(rnorm(numInstances / 2 * numDiscrete, mean=0)), nrow=numInstances / 2, ncol=numDiscrete)
    dataMatrix21 = matrix(discretize(rnorm(numInstances / 4 * numDiscreteSignal, mean=group2Mean)), nrow=numInstances / 4, ncol=numDiscreteSignal)
    dataMatrix22 = matrix(discretize(rnorm(numInstances / 4 * numDiscreteRandom, mean=0)), nrow=numInstances / 4, ncol=numDiscreteRandom)
    dataMatrix31 = matrix(discretize(rnorm(numInstances / 4 * numDiscreteSignal, mean=-group2Mean)), nrow=numInstances / 4, ncol=numDiscreteSignal)
    dataMatrix32 = matrix(discretize(rnorm(numInstances / 4 * numDiscreteRandom, mean=0)), nrow=numInstances / 4, ncol=numDiscreteRandom)

    discreteMatrix = rbind(dataMatrix1, cbind(dataMatrix21, dataMatrix22))
    discreteMatrix = rbind(discreteMatrix, cbind(dataMatrix31, dataMatrix32))
  }

  data = as.data.frame(cbind(continuousMatrix, discreteMatrix))

  colnames(data) = paste("Feature", 1:ncol(data), sep="")
  rownames(data) = paste("Instance", 1:nrow(data), sep="")

  # Add a few missing values
  for (i in 1:10)
    data[sample(1:nrow(data))[1], sample(1:ncol(data))[1]] <- NA

  classValues = c(rep(1, numInstances / 2), rep(2, numInstances / 4), rep(3, numInstances / 4))

  classData = as.data.frame(matrix(classValues, ncol=1))
  colnames(classData) = "Class"

  data <- cbind(data, classData)

  outDataFile = gzfile(outDataFilePath, "w")

  write.table(data, outDataFile, sep="\t", row.names=T, col.names=NA, quote=F)

  close(outDataFile)
}

discretize <- function(x)
{
  sapply(x, function(y) {
    if (y < -1)
      return("Low")
    if (y > 1)
      return("High")
    return("Medium")
  })
}

generate(95, 5, 0, 0, 60, "NoSignal_Continuous", 0)
#generate(95, 5, 0, 0, 60, "MediumSignal_Continuous", 1)
generate(95, 5, 0, 0, 60, "StrongSignal_Continuous", 5)

generate(0, 0, 95, 5, 60, "NoSignal_Discrete", 0)
#generate(0, 0, 95, 5, 60, "MediumSignal_Discrete", 1)
generate(0, 0, 95, 5, 60, "StrongSignal_Discrete", 5)

generate(45, 5, 45, 5, 60, "NoSignal_Both", 0)
#generate(45, 5, 45, 5, 60, "MediumSignal_Both", 1)
generate(45, 5, 45, 5, 60, "StrongSignal_Both", 5)

generate(9995, 5, 9995, 5, 60, "StrongSignalLarge_Both", 5)
