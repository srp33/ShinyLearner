library(knitr)
library(AUC)
library(rmarkdown)
library(readr)

# Command line arguments (1 = 6)
predictionsFile <- commandArgs()[6]
metricsFile <- commandArgs()[7]
outputReportFile <- commandArgs()[8]
version <- readChar('VERSION', file.info('VERSION')$size)

print(predictionsFile)
print(metricsFile)
print(outputReportFile)
print(version)

# We only want the probabilities for the ensemble_majority_vote algorithm
preds <- read_tsv(predictionsFile)
preds <- preds[preds$Algorithm=='Ensemble_Majority_Vote',]

print(head(preds))

# The final columns of the header are the class probabilities
classes <- colnames(preds)[7:length(colnames(preds))]
# InstanceIDs and class probabilities
preds_p <- preds[,c('InstanceID',classes)]
# Mean probabilities for each InstanceID
preds_p <- aggregate(preds_p, by=list(preds_p$InstanceID), FUN=mean)[,c('Group.1',classes)]

# InstanceIDs and actual classes
preds_a <- preds[,c('InstanceID','ActualClass')]
# Mean actual class for each InstanceID (should be identical for each, so this step is to essentially remove duplicate InstanceIDs)
preds_a <- aggregate(preds_a, by=list(preds_a$InstanceID), FUN=mean)[,c('Group.1','ActualClass')]

# InstanceIDs, actual classes, and mean probabilities (from ensemble_majority_vote algorithm)
preds_ap <- merge(preds_a, preds_p, by="Group.1")

# Number the rows
rownames(preds_ap) <- seq(length=nrow(preds_ap))

# We only want metrics from the ensemble_majority_vote algorithm
mets <- read_tsv(metricsFile)
mets <- mets[mets$Algorithm=='Ensemble_Majority_Vote',]

# Mean value for each metric across all iterations for ensemble_majority_vote
mets_a <- mets[,c('Metric','Value')]
mets_a <- aggregate(mets_a, by=list(mets_a$Metric), FUN=mean)[,c('Group.1','Value')]

# ROC Curve
getROCC <- function(classNumber, multiclass){
  actuals_classNumber <- as.factor(as.integer(preds$ActualClass==classes[classNumber]))
  if (multiclass)
    class <- paste(classes[classNumber], 'vs', 'All')
  if (!multiclass)
    class <- paste(classes[classNumber], 'vs', classes[classNumber - 1])	
  rocc_classNumber <- roc(preds[[(6+classNumber)]],actuals_classNumber)
  rocc_classNumber <- data.frame('class'=class,'fpr'=rocc_classNumber$fpr,'tpr'=rocc_classNumber$tpr)
  return(rocc_classNumber)
}
if (length(classes) == 2) {
  rocc <- getROCC(2,FALSE)
}
if (length(classes) > 2){
  rocc <- getROCC(1,TRUE)
  for (i in seq(from=2, to=length(classes))){
	rocc <- rbind(rocc, getROCC(i,TRUE))
  }
}
random_line <- data.frame('class'='(Random Accuracy)','fpr'=c(0,1),'tpr'=c(0,1))
rocc <- rbind(random_line, rocc)


# RENDER
render('scripts/render_report_nestedclassification.Rmd', output_file=paste('..', outputReportFile, sep='/'), params=list(
  p=preds_ap,
  m=mets_a,
  v=version,
  r=rocc
))
