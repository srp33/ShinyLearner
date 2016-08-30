library(shiny)
library(readr)
library(dplyr)

shinyServer(function(input, output, session) {

clfNames <- read_tsv('meta/classifier_names_all.tsv')
shiny_script <- NULL
description <- NULL

# Prepare Script (on button click)
observeEvent(input$button_script, {
  shared_dir <- input$shared_dir
  class_file <- input$class_file
  mol_file <- input$molecular_file
  dataFiles <- paste(paste('v',class_file,sep='/'), paste('v',mol_file,sep='/'), sep=',')
  outerNumIterations <- 5
  innerNumIterations <- 2
  debug <- 'false'
  use_default_parameters <- 'true'
  classifAlgos <- c('s_random_forest','s_svm_linear')
  classifAlgos <- paste(filter(clfNames,(clfNames$classifier %in% classifAlgos))$script, collapse=',') 
  class_options <- paste("\"",input$class_options,"\"",sep='')
  exp_name <- paste("\"",input$exp_name,"\"",sep='')
  description <- gsub('[^[:alnum:]]','_',input$exp_name)
  shiny_script <<- paste(paste('docker run --rm -v $(pwd)/',shared_dir,':/ShinyLearner/v shiny_learner',sep=''), dataFiles, description, outerNumIterations, innerNumIterations, debug, classifAlgos, use_default_parameters, class_options, exp_name)
})

# Display Scripts
getShinyScript <- eventReactive(input$button_script,{
  shiny_script
})
output$shiny_script <- renderText({
  getShinyScript()
})
})