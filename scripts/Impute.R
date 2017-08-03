hasOnlyIntegers <- function(x)
{
  y <- sapply(x, function(z) { is.na(z) | z%%1 == 0 })
  return(all(y))
}

    acceptableProportionMissing = 0.2
    
    # How many missing?
    proportionMissing <- nrow(filter_(dataToSave, paste("is.na(", queryColumnName, ")"))) / nrow(dataToSave)
    
    if (proportionMissing > acceptableProportionMissing)
    {
      print(paste(proportionMissing, " of the values were missing for ", queryColumnName, ", so these data cannot be used as a covariate.", sep=""))
      return(NULL)
    }

    # Impute
    print(paste("Imputing any missing values for column ", queryColumnName, sep=""))
    library(mlr)
    dataToSave <- impute(dataToSave, classes = list(numeric = imputeMedian(), integer = imputeMedian(), factor = imputeMode()), impute.new.levels=FALSE)$data
    
    if (is.factor(dataToSave[,queryColumnName])) {
      print("Dummifying discrete variables")
      dataToSave <- dummify(dataToSave, queryColumnName)
    } else {
      print("Standardizing continuous variables")
      dataToSave[,queryColumnName] <- standardize(dataToSave[,queryColumnName], queryColumnName)
      colnames(dataToSave)[which(colnames(dataToSave) == queryColumnName)] <- queryColumnName
    }
  }
