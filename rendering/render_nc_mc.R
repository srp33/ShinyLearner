library(knitr)
library(AUC)
library(RankAggreg)
library(rmarkdown)
library(readr)

# Arguments (1st arg is 6)
tempOutDir <- commandArgs()[6]
outerNumIterations <- commandArgs()[7]
outPredictionsFile <- paste(tempOutDir,'Predictions.tsv',sep='/')
preds <- read_tsv(outPredictionsFile)
preds$ActualClass <- as.factor(preds$ActualClass)
outMetricsFile <- paste(tempOutDir,'Metrics.tsv',sep='/')
metrics <- read_tsv(outMetricsFile)
class_options <- strsplit(commandArgs()[8],',')[[1]]
exp_name <- commandArgs()[9]
version <- readChar('Version.txt', file.info('Version.txt')$size)

# Predictions
numeric_classes <- colnames(preds)[7:(6+length(class_options))]
colnames(preds) <- c(colnames(preds)[0:6],class_options)
for (i in seq(1, length(class_options))){
  preds[5:6] <- as.data.frame(lapply(preds[5:6], function(x) {gsub(paste("^",numeric_classes[i],"$",sep=""), class_options[i], x)}))
}
p_table <- preds[,c('InstanceID',class_options)]
p_table <- aggregate(p_table, by=list(p_table$InstanceID), FUN=mean)[,c('Group.1',class_options)]
colnames(p_table) <- c('InstanceID',class_options)
actuals <- preds[,c('InstanceID','ActualClass')]
p_table <- merge(p_table, actuals, by="InstanceID")
p_table <- p_table[ order(p_table[,1]), ]
rownames(p_table) <- seq(length=nrow(p_table))
p_table <- p_table[1:10,c('InstanceID','ActualClass',class_options)]
colnames(p_table) <- c('Sample','Actual Class', class_options)

auc <- metrics[metrics$Metric == 'AUROC', ][,c('Iteration','Value')]
auc <- aggregate(auc, by=list(auc$Iteration), FUN = mean)[,c('Iteration','Value')]
auc$Metric <- 'Area Under the ROC Curve'
tpr <- metrics[metrics$Metric == 'TPR', ][,c('Iteration','Value')]
tpr <- aggregate(tpr, by=list(tpr$Iteration), FUN = mean)[,c('Iteration','Value')]
tpr$Metric <- 'True Positive Rate'
fpr <- metrics[metrics$Metric == 'FPR', ][,c('Iteration','Value')]
fpr <- aggregate(fpr, by=list(fpr$Iteration), FUN = mean)[,c('Iteration','Value')]
fpr$Metric <- 'False Positive Rate'

# Iteration Metrics
iteration_metrics <- data.frame(auc$Value,tpr$Value,fpr$Value)
colnames(iteration_metrics) <- c('Area Under the ROC Curve','True Positive Rate','False Positive Rate')
rownames(iteration_metrics) <- paste('Iteration',seq(length=nrow(iteration_metrics)))
#
# Average Metrics
average_metrics <- NULL
if (outerNumIterations > 1){
  auc_t <- t.test(auc$Value)
  tpr_t <- t.test(tpr$Value)
  fpr_t <- t.test(fpr$Value)
  average_metrics <- data.frame(c('Area Under the ROC Curve','True Positive Rate','False Positive Rate'),c(auc_t$estimate,tpr_t$estimate,fpr_t$estimate),c(auc_t$conf.int[1],tpr_t$conf.int[1],fpr_t$conf.int[1]),c(auc_t$conf.int[2],tpr_t$conf.int[2],fpr_t$conf.int[2]))
  colnames(average_metrics) <- c('Metric','Mean Across Iterations','95% Confidence Interval','')
}

# ROC Curve
getROCC <- function(classNumber, multiclass){
  actuals_classNumber <- as.factor(as.integer(preds$ActualClass==class_options[classNumber]))
  if (multiclass)
    class_option <- paste(class_options[classNumber], 'vs', 'All')
  if (!multiclass)
    class_option <- paste(class_options[classNumber], 'vs', class_options[classNumber - 1])	
  rocc_classNumber <- roc(preds[[(6+classNumber)]],actuals_classNumber)
  rocc_classNumber <- data.frame('class'=class_option,'fpr'=rocc_classNumber$fpr,'tpr'=rocc_classNumber$tpr)
  return(rocc_classNumber)
}
if (length(class_options) == 2) {
  rocc <- getROCC(2,FALSE)
}
if (length(class_options) > 2){
  rocc <- getROCC(1,TRUE)
  for (i in seq(from=1, to=length(class_options))){
	rocc <- rbind(rocc, getROCC(i,TRUE))
  }
}
random_line <- data.frame('class'='(Random Accuracy)','fpr'=c(0,1),'tpr'=c(0,1))
rocc <- rbind(random_line, rocc)

# rmarkdown
render('render_nc_mc.Rmd', output_file=paste(tempOutDir,'/',tempOutDir,'.html',sep=''), params=list(
  exp_name = exp_name,
  outerNumIterations = outerNumIterations,
  version=version,
  rocc=rocc,
  iteration_metrics=iteration_metrics,
  average_metrics=average_metrics,
  preds=preds
))
