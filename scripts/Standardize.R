standardize <- function(values, columnName)
{
  if (hasOnlyIntegers(values) & length(unique(values)) < 10)
  {
    print(paste("The ", columnName, " column contains integers but fewer than 10 distinct values, so it does not need to be standardized.", sep=""))
    return(values)
  }
  
  print(paste("Standardizing values for column ", columnName, sep=""))
  
  return(scale(values))
}

hasOnlyIntegers <- function(x)
{
  y <- sapply(x, function(z) { is.na(z) | z%%1 == 0 })
  return(all(y))
}

      dataToSave[,queryColumnName] <- standardize(dataToSave[,queryColumnName], queryColumnName)
      colnames(dataToSave)[which(colnames(dataToSave) == queryColumnName)] <- queryColumnName
