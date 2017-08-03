library(shiny)

shinyServer(function(input, output, session) {
  
  dockerhub_address <- 'srp33/shinylearner:version331'
  numFeaturesOptions <- '5,10,50,100,500,1000'
  defaultInputFiles <- 'Data.tsv.gz'
  defaultInputFiles <- 'StrongSignal_Both.tsv.gz'
  defaultOutputDir <- 'Output'
  defaultExpDesc <- 'My_Interesting_Analysis'
  defaultValidation <- 'mc'
  validationChoices <- list('Monte-Carlo Cross Validation' = 'mc', 'k-Fold Cross Validation' = 'kf')
  defaultFS <- 'no_fs'
  defaultInnerIterations <- 5
  mc_inner_options <- list(5,10)
  defaultOuterIterations <- 10
  mc_outer_options <- list(1,5,10,100)
  defaultInnerFolds <- 5
  kf_inner_options <- list(5,10)
  defaultOuterFolds <- 10
  kf_outer_options <- list(5,10)
  defaultIterations <- 1
  kf_iterations_options <- list(1,5,10,100)
  defaultOS <- 'linux/mac'
  osOptions <- list('Linux or Mac' = 'linux/mac', 'Windows' = 'windows')
  defaultFSAlgos <- 'AlgorithmScripts/FeatureSelection/tsv/sklearn/anova'
  defaultFSOpt <- FALSE
  defaultClassifAlgos <- 'AlgorithmScripts/Classification/tsv/sklearn/svm'
  defaultClassifOpt <- FALSE
  defaultOHE <- FALSE
  defaultStan <- FALSE
  defaultSeed <- ''
  defaultImpute <- FALSE
  defaultContainerInputDir <- 'InputData'
  defaultContainerOutputDir <- 'OutputData'

  
  exp_desc_help_text <- 'Please enter a short, unique description of the analysis.'
  input_files_help_text <- 'Please indicate the location on your computer of the input data files that will be used in the analysis. If the file(s) are located in a subdirectory, please also specify the name of that subdirectory in the file path(s). Wildcards are allowed, and the files may be gzipped. Input files can be in comma-separated (.csv), tab-separated (.tsv) or Attribute-Relation File Format (.arff). If you use .csv or .tsv files, rows should be samples, and columns should be features (independent variables). If you specify multiple paths, separate them by commas. [If you wish to use an input file format that is not supported, please contact us.]'
  output_dir_help_text <- 'Please specify a directory where the output files will be stored after ShinyLearner executes. Multiple output files will be created that contain the results of the analysis.'
  validation_help_text <- 'An important aspect of supervised machine learning is to assess how well the algorithmic predictions will generalize (make successful predictions on new data). ShinyLearner supports two ways of assessing generalizability: Monte Carlo cross validation and k-fold cross validation. You can read more about these methods <a target="_blank" href="https://en.wikipedia.org/wiki/Cross-validation_(statistics)"><b>here</b></a>. The Monte Carlo method randomly assigns samples to training and testing sets and repeats this process for many iterations. The k-fold method assigns samples to training and testing sets such that each sample is tested exactly once per iteration.'
  feat_sel_help_text <- 'Feature selection seeks to identify features (independent variables) that are most important. Oftentimes, reducing the size of the data via feature selection leads to higher accuracy. Feature selection may also make it easier for a human to understand more about which parts of the data are most important. However, feature selection does increase the computer-execution time.'
  sel_classifAlgos_help_text <- '(Optimization will increase runtime but will likely be more accurate). Choose one or more classification algorithms. ShinyLearner has integrated a wide variety of algorithms from other software packages. You can learn more about these algorithms <a target="_blank" href="https://github.com/srp33/ShinyLearner/blob/master/Algorithms.md"><b>here</b></a>. Please let us know if you would like us to support additional algorithms (or hyperparameters).'
  sel_fsAlgos_help_text <- '(Optimization will increase runtime but will likely be more accurate). Choose one or more feature-selection algorithms. ShinyLearner has integrated a wide variety of algorithms from other software packages. You can learn more about these algorithms <a target="_blank" href="https://github.com/srp33/ShinyLearner/blob/master/Algorithms.md"><b>here</b></a>. Please let us know if you would like us to support additional algorithms (or hyperparameters).'
  os_help_text <- 'ShinyLearner will be executed within a "software container" (explanation <a target="_blank" href="https://gigascience.biomedcentral.com/articles/10.1186/s13742-016-0135-4"><b>here</b></a> using the <a target="_blank" href="https://www.docker.com">Docker</a> technology. Docker can be executed on many operating systems, including Mac OS, Windows, and Linux. But the command that you use to execute Docker may be different, depending on the operating system.'
  script_help_text <- 'Copy this script into a terminal / command prompt after turning on Docker.'
  mc_help_text <- 'Machine-learning analyses can be executed in multiple iterations. When multiple iterations are used, it helps with estimating the consistency of the results across multiple partitions of the data. "Inner" iterations are used to optimize algorithm choice on the training data. Using multiple iterations can help ensure that algorithm choice is robust. "Outer" iterations indicate the number of times that the overall process (training and testing) are performed. A larger number of iterations should lead to more robust results but will also increase computational time.'
  kf_help_text <- 'Machine-learning analyses can be executed in multiple iterations. When multiple iterations are used, it helps with estimating the consistency of the results across multiple partitions of the data. "Inner" iterations are used to optimize algorithm choice on the training data. Using multiple iterations can help ensure that algorithm choice is robust. "Outer" iterations indicate the number of times that the overall process (training and testing) are performed. A larger number of iterations should lead to more robust results but will also increase computational time.'
  ohe_help_text <- 'One-Hot-Encoding does the following...'
  stan_help_text <- 'Standardization modifies the data to facilitate better machine-learning results...'
  seed_help_text <- 'Manually set the NUMERICAL random seed...'
  impute_help_text <- 'Impute missing values...'
  
  help_icon <- icon('lightbulb-o', 'fa-1x')
  
  
  ## Get Algorithms from File System
  prefix <- function(x) {
    return(paste(strsplit(x, '/')[[1]][c(3,4,5,6,7)], collapse='/'))
  }
  short_names <- function(x) {
    return(paste(strsplit(x, '/')[[1]][c(4,5)], collapse='/'))
  }
  # Get Classifier and Features Selector options from files system and sort by name
  classifAlgosOptions <-  list.dirs(path='./ShinyLearner/AlgorithmScripts/Classification', recursive=TRUE)
  classifAlgosOptions <- classifAlgosOptions[sapply(classifAlgosOptions, function(x) length(list.dirs(x, recursive = FALSE)) == 0)] # https://stackoverflow.com/questions/41961474/list-leaf-directories-in-r
  classifAlgosOptions <- lapply(classifAlgosOptions, prefix) 
  names(classifAlgosOptions) <- lapply(classifAlgosOptions, short_names)
  classifAlgosOptions <- classifAlgosOptions[order(unlist(names(classifAlgosOptions)))]
  fsAlgosOptions <-  list.dirs(path='./ShinyLearner/AlgorithmScripts/FeatureSelection', recursive=TRUE)
  fsAlgosOptions <- fsAlgosOptions[sapply(fsAlgosOptions, function(x) length(list.dirs(x, recursive = FALSE)) == 0)] # https://stackoverflow.com/questions/41961474/list-leaf-directories-in-r
  fsAlgosOptions <- lapply(fsAlgosOptions, prefix)
  names(fsAlgosOptions) <- lapply(fsAlgosOptions, short_names)
  fsAlgosOptions <- fsAlgosOptions[order(unlist(names(fsAlgosOptions)))]

  # Initializations    
  shiny_script <- ''
  
# (1) Subpage
  ## Experiment Description
  output$exp_desc_textbox_ui <-renderUI({
	textInput("exp_desc_textbox", NULL, value=defaultExpDesc, width='100%')
  })
  ## Experiment Description Help
  output$exp_desc_help_button_ui <- renderUI({
	#actionButton('exp_desc_help_button','', icon=help_icon)
  })
  output$exp_desc_help_message_ui <- renderUI({
	#if (length(input$exp_desc_help_button) != 0 && (input$exp_desc_help_button) %% 2 == 1){
	  helpText(HTML(exp_desc_help_text))
	#} else return()
  })
  ## Input Files
  output$input_files_textbox_ui <-renderUI({
	textInput("input_files_textbox", NULL, value=defaultInputFiles, width='100%')
  })
  ## Input Files Help
  output$input_files_help_button_ui <- renderUI({
	#actionButton('input_files_help_button','', icon=help_icon)
  })
  output$input_files_help_message_ui <- renderUI({
	#if (length(input$input_files_help_button) != 0 && (input$input_files_help_button) %% 2 == 1){
	  helpText(HTML(input_files_help_text))
	#} else return()
  })
  ## Output Directory
  output$output_dir_textbox_ui <-renderUI({
	textInput("output_dir_textbox", NULL, value=defaultOutputDir, width='100%')
  })
  ## Output Files Help
  output$output_dir_help_button_ui <- renderUI({
	#actionButton('output_dir_help_button','', icon=help_icon)
  })
  output$output_dir_help_message_ui <- renderUI({
	#if (length(input$output_dir_help_button) != 0 && (input$output_dir_help_button) %% 2 == 1){
	  helpText(HTML(output_dir_help_text))
	#}else return()
  })
  

# (2) Subpage
  ## Choose Validation UI
  output$validation_radio_ui <- renderUI({
	radioButtons('validation_radio', NULL, validationChoices, selected=defaultValidation)
  })
  output$validation_help_button_ui <- renderUI({
	#actionButton('validation_help_button','', icon=help_icon)
  })
  output$validation_help_message_ui <- renderUI({
	#if (length(input$validation_help_button) != 0 && (input$validation_help_button) %% 2 == 1){
	  helpText(HTML(validation_help_text))
	#} else return()
  })
  ## Choose Feature Selection UI
  output$feat_sel_radio_ui <- renderUI({
	radioButtons('feat_sel_radio', NULL, list('Yes' = 'fs', 'No' = 'no_fs'), selected=defaultFS)
  })
  output$feat_sel_help_button_ui <- renderUI({
	#actionButton('feat_sel_help_button', '', icon=help_icon)
  })
  output$feat_sel_help_message_ui <- renderUI({
	#if (length(input$feat_sel_help_button) != 0 && (input$feat_sel_help_button) %% 2 == 1){
	  helpText(HTML(feat_sel_help_text))
	#} else return()
  })

# (3) Subpage
  ## MC Inner Iterations
  output$mc_inner_iterations_radio_ui <- renderUI({ 
	if (length(input$validation_radio) != 0 && input$validation_radio == 'mc') {
	  radioButtons('mc_inner_iterations_radio', 'Choose Number of Inner Iterations:', mc_inner_options, selected = defaultInnerIterations)
	}
  })
  ## MC Outer Iterations
  output$mc_outer_iterations_radio_ui <- renderUI({
	if (length(input$validation_radio) != 0 && input$validation_radio == 'mc') {
	  radioButtons('mc_outer_iterations_radio', 'Choose Number of Outer Iterations:', mc_outer_options, selected=defaultOuterIterations)
	}
  })
  ## KF Inner Folds
  output$kf_inner_folds_radio_ui <- renderUI({
	if (length(input$validation_radio) != 0 && input$validation_radio == 'kf')
	  radioButtons('kf_inner_folds_radio', 'Choose Number of Inner Folds:', kf_inner_options, selected=defaultInnerFolds)
  })
  ## KF Outer Folds
  output$kf_outer_folds_radio_ui <- renderUI({
	if (length(input$validation_radio) != 0 && input$validation_radio == 'kf')
	  radioButtons('kf_outer_folds_radio', 'Choose Number of Outer Folds:', kf_outer_options, selected=defaultOuterFolds)
  })
  ## KF Iterations
  output$kf_iterations_radio_ui <- renderUI({
	if (length(input$validation_radio) != 0 && input$validation_radio == 'kf')
	  radioButtons('kf_iterations_radio', 'Choose Number of Iterations:', kf_iterations_options, selected=defaultIterations)
  })
  ## Validation Settings Help
  output$val_settings_help_button_ui <- renderUI({
	#actionButton('val_settings_help_button','',icon=help_icon)
  })
  output$val_settings_help_message_ui <- renderUI({
	if (length(input$validation_radio) != 0 && input$validation_radio == 'mc') {
	  #if (length(input$val_settings_help_button) != 0 && (input$val_settings_help_button) %% 2 == 1) {
	    helpText(HTML(mc_help_text))
	  #}
	} else if (length(input$validation_radio) != 0 && input$validation_radio == 'kf') {
	  #if (length(input$val_settings_help_button) != 0 && (input$val_settings_help_button) %% 2 == 1) {
	    helpText(HTML(kf_help_text))
	  #}
	}
  })
  
# (4) Subpage
  ## Classification Algorithm
  output$sel_classifAlgos_ui <- renderUI({
    selectizeInput('sel_classifAlgos', NULL, choices = classifAlgosOptions, multiple = TRUE, selected=defaultClassifAlgos)
  })
  output$sel_classifOpt_ui <- renderUI({
    checkboxInput('sel_classifOpt', 'Optimize Parameters?', value = defaultClassifOpt)
  })
  output$sel_classifAlgos_header_ui <- renderUI({
    h4('Classification Algorithms')
  })
  output$sel_classifAlgos_help_button_ui <- renderUI({
    #actionButton('sel_classifAlgos_help_button','',icon=help_icon)
  })
  output$sel_classifAlgos_help_message_ui <- renderUI({
	#if (length(input$sel_classifAlgos_help_button) != 0 && (input$sel_classifAlgos_help_button) %% 2 == 1) {
	  helpText(HTML(sel_classifAlgos_help_text))
	#} else {return()}
  })
  output$sel_fsAlgos_ui <- renderUI({
    if (length(input$feat_sel_radio) != 0 && input$feat_sel_radio == 'fs') {
      selectizeInput('sel_fsAlgos', NULL, choices = fsAlgosOptions, multiple = TRUE, selected=defaultFSAlgos)
    } else {return()}
  })
  output$sel_FSOpt_ui <- renderUI({
    if (length(input$feat_sel_radio) != 0 && input$feat_sel_radio == 'fs') {
      checkboxInput('sel_FSOpt', 'Optimize Parameters?', value = defaultFSOpt)
    } else {return()}
  })
  output$sel_fsAlgos_header_ui <- renderUI({
    if (length(input$feat_sel_radio) != 0 && input$feat_sel_radio == 'fs') {
      h4('Feature Selection Algorithms')
    } else {return()}
  })
  output$sel_fsAlgos_help_button_ui <- renderUI({
    if (length(input$feat_sel_radio) != 0 && input$feat_sel_radio == 'fs') {
      #actionButton('sel_fsAlgos_help_button','',icon=help_icon)
    } else {return()}
  })
  output$sel_fsAlgos_help_message_ui <- renderUI({
    if (length(input$feat_sel_radio) != 0 && input$feat_sel_radio == 'fs') {
	  #if (length(input$sel_fsAlgos_help_button) != 0 && (input$sel_fsAlgos_help_button) %% 2 == 1) {
	    helpText(HTML(sel_fsAlgos_help_text))
	  #} else {return()}
	} else {return()}
  })

  # (5) Subpage
  ## One-Hot-Encoding
  output$ohe_checkbox_ui <- renderUI({
    checkboxInput('ohe_checkbox', 'One-Hot-Encoding', value = defaultOHE)
  })
  output$ohe_help_message_ui <- renderUI({
    helpText(HTML(ohe_help_text))
  })
  ## Standardize Data
  output$stan_checkbox_ui <- renderUI({
    checkboxInput('stan_checkbox', 'Standardize Data', value = defaultStan)
  })
  output$stan_help_message_ui <- renderUI({
    helpText(HTML(stan_help_text))
  })
  ## Standardize Data
  output$impute_checkbox_ui <- renderUI({
    checkboxInput('impute_checkbox', 'Impute Missing Data', value = defaultImpute)
  })
  output$impute_help_message_ui <- renderUI({
    helpText(HTML(impute_help_text))
  })
  ## Set Random Seed
  output$seed_textbox_ui <- renderUI({
    textInput('seed_textbox', 'Random Seed', value = defaultSeed, placeholder='[Leave blank to use default seed]')
  })
  output$seed_help_message_ui <- renderUI({
    helpText(HTML(seed_help_text))
  })


  # (6) Subpage
  ## Operating System
  output$os_ui <- renderUI({
	radioButtons('os_radio', NULL, osOptions, selected=defaultOS)
  })
  ## Opearting System Help
  output$os_help_button_ui <- renderUI({
	#actionButton('os_help_button','', icon=help_icon)
  })
  output$os_help_message_ui <- renderUI({
	#if (length(input$os_help_button) != 0 && (input$os_help_button) %% 2 == 1){
	  helpText(HTML(os_help_text))
	#} else return()
  })
  ## Display Command
  ## This function synthesizes all of the user's input, and assigns the resulting string to the global variable 'shiny_scrpt'.
  ## There is a lot of logic/conditionals in order to robustly interpret input from the GUI.
  ## I've tried to design it such that we need not alter it frequently, as long as the UserScripts remain the same.
  ## Most parameters are available at the top of the page instead.
  output$shiny_script <- renderText({
  
    ## Get Values from UIs 
    validation <- ''
    if (length(input$validation_radio) != 0 && input$validation_radio == 'mc')
      validation <- 'mc'
    if (length(input$validation_radio) != 0 && input$validation_radio == 'kf')
      validation <- 'kf'
      
    fs <- ''
    if (length(input$feat_sel_radio) != 0 && input$feat_sel_radio == 'fs')
      fs <- 'fs'
    if (length(input$feat_sel_radio) != 0 && input$feat_sel_radio == 'no_fs')
      fs <- 'no_fs'
    
    mc_outer <- ''
    if (length(input$mc_outer_iterations_radio != 0))
      mc_outer <- input$mc_outer_iterations_radio

    mc_inner <- ''
    if(length(input$mc_inner_iterations_radio != 0))
      mc_inner <- input$mc_inner_iterations_radio
      
    kf_iterations <- ''
    if (length(input$kf_iterations_radio) != 0)
      kf_iterations <- input$kf_iterations_radio
    
    kf_outer <- ''
    if (length(input$kf_outer_folds_radio) != 0)
      kf_outer <- input$kf_outer_folds_radio
      
    kf_inner <- ''
    if (length(input$kf_inner_folds_radio) != 0)
      kf_inner <- input$kf_inner_folds_radio
      
    if (validation == '')
      validation <- defaultValidation
    if (fs == '')
      fs <- defaultFS
    if (mc_outer == '')
      mc_outer <- defaultOuterIterations
    if (mc_inner == '')
      mc_inner <- defaultInnerIterations
    if (kf_iterations == '')
      kf_iterations <- defaultIterations
    if (kf_outer == '')
      kf_outer <- defaultOuterFolds
    if (kf_inner == '')
      kf_inner <- defaultInnerFolds
      
    seed <- ''
    if (!is.null(input$seed_textbox) && input$seed_textbox != '' && !is.na(as.integer(input$seed_textbox))) {
      seed <- as.integer(input$seed_textbox)
    } else {
      seed <- defaultSeed
    }
      
    ohe <- 'false'
    if (!is.null(input$ohe_checkbox) && input$ohe_checkbox == TRUE) {
      ohe <- 'true'
    }
    
    stan <- 'false'
    if (!is.null(input$stan_checkbox) && input$stan_checkbox == TRUE) {
      stan <- 'true'
    }
    
    impute <- 'false'
    if (!is.null(input$impute_checkbox) && input$impute_checkbox == TRUE) {
      impute <- 'true'
    }
    
      
    ## Determine FS Algos
    fsAlgos <- input$sel_fsAlgos
    if (!is.null(input$sel_FSOpt) && input$sel_FSOpt == TRUE) {
      fsAlgos <- lapply(fsAlgos, function(x) {paste(x, '/*', sep='')})
    } else {
      fsAlgos <- lapply(fsAlgos, function(x) {paste(x, '/default*', sep='')})
    }
    fsAlgos <- paste(fsAlgos, collapse=',')
    if (fsAlgos == '') {
      fsAlgos = defaultFSAlgos
    }

    ## Determine Classif Algos
    classifAlgos <- input$sel_classifAlgos
    if (!is.null(input$sel_classifOpt) && input$sel_classifOpt == TRUE) {
      classifAlgos <- lapply(classifAlgos, function(x) {paste(x, '/*', sep='')})
    } else {
      classifAlgos <- lapply(classifAlgos, function(x) {paste(x, '/default*', sep='')})
    }
    classifAlgos <- paste(classifAlgos, collapse=',')
    if (classifAlgos == '') {
      classifAlgos = defaultClassifAlgos
    }
    
    
    ## Establish OS
    os <- ''
    os_pwd <- ''
    if (length(input$os_radio) != 0 && input$os_radio == 'linux/mac') {
      os <- 'linux/mac'
    } else if (length(input$os_radio) != 0 && input$os_radio == 'windows') {
      os <- 'windows'
    }
    if (os == '')
      os <- defaultOS      
    if (os == 'linux/mac')
      os_pwd <- '$(pwd)/'
    if (os == 'windows')
      os_pwd <- '%cd%\\'


    
    ## Paths
	containerInputDir <- defaultContainerInputDir
	containerOutputDir <- defaultContainerOutputDir
    hostInputDir <- input$input_files_textbox
    hostInputFileName <- input$input_files_textbox
    hostOutputDir <- input$output_dir_textbox
    expDesc <- input$exp_desc_textbox
    
    ## Replace ' ' with '_'
    hostInputDir <- gsub(' ', '_', hostInputDir)
    hostInputFileName <- gsub(' ', '_', hostInputFileName)
    hostOutputDir <- gsub(' ', '_', hostOutputDir)
    expDesc <- gsub(' ', '_', expDesc)
    
    ## Use defaults if no entry
	if (hostInputDir == '') {hostInputDir = defaultInputFiles}
	if (hostInputFileName == '') {hostInputFileName == defaultInputFiles}
	if (hostOutputDir == '') {hostOutputDir = defaultOutputDir}
	if (expDesc == '') {expDesc = defaultExpDesc}
	
	## Split for Multiple Input Files
    hostInputDir <- strsplit(hostInputDir, ',')
    hostInputFileName <- strsplit(hostInputFileName, ',')
    
	## Replace '\' with '/' and parse directories/filenames
	## Check for '~' and do not allow dirname/basename to transform '~' to the home directory
	## Check for '.' when used as a file extension.
	hostInputDir <- lapply(hostInputDir, FUN = function(x) gsub('~', 'TILDE_ESCAPE', x))
	hostInputDir <- lapply(hostInputDir, FUN = function(x) gsub('\\.', 'DOT_ESCAPE', x))
	hostInputFileName <- lapply(hostInputFileName, FUN = function(x) gsub('~', 'TILDE_ESCAPE', x))
	hostInputFileName <- lapply(hostInputFileName, FUN = function(x) gsub('\\.', 'DOT_ESCAPE', x))
	hostInputDir <- lapply(hostInputDir, FUN = function(x) gsub('\\.', '', dirname(gsub('\\\\', '/', x))))
	hostInputFileName <- lapply(hostInputFileName, FUN = function(x) gsub('\\.', '', (basename(gsub('\\\\', '/', x)))))
	hostInputDir <- lapply(hostInputDir, FUN = function(x) gsub('TILDE_ESCAPE', '~', x))
	hostInputDir <- lapply(hostInputDir, FUN = function(x) gsub('DOT_ESCAPE', '\\.', x))
	hostInputFileName <- lapply(hostInputFileName, FUN = function(x) gsub('TILDE_ESCAPE', '~', x))
	hostInputFileName <- lapply(hostInputFileName, FUN = function(x) gsub('DOT_ESCAPE', '\\.', x))
	hostOutputDir <- gsub('\\\\', '/', hostOutputDir)
	
	## Trim trailing '/'
	if (substr(hostOutputDir, nchar(hostOutputDir), nchar(hostOutputDir)) == '/') {
	  hostOutputDir <- substr(hostOutputDir, 0, nchar(hostOutputDir)-1)
	} 
	lines <- list()
	## Windows
    if (os == 'windows') {
      ## replace '/' with '\'
	  hostInputDir <- lapply(hostInputDir, FUN = function(x) gsub('/', '\\\\', x))
	  hostInputDir <- lapply(hostInputDir, FUN = function(x) gsub('.', '', x))
	  hostInputFileName <- lapply(hostInputFileName, FUN = function(x) gsub('/', '\\\\', x))
	  hostOutputDir = gsub('/', '\\\\', hostOutputDir)
	  lines <- c(lines, 'docker run --rm')
	  ## Mount Input Dirs
	  for (i in 1:length(hostInputDir[[1]])){
	    if (i > 1) {break} # currently only support one input direcory
		if (substr(hostInputDir[[1]][i], 2, 2) == ':') {
		  ## Root Directory ('C:')
		  if (nchar(hostInputDir[[1]][i]) == 2) {
		    lines <- c(lines, paste('-v ', hostInputDir[[1]][i] , '\\',  ':/', containerInputDir, sep=''))
		  ## Absolute Path
		  } else {
			lines <- c(lines, paste('-v ', hostInputDir[[1]][i] , ':/', containerInputDir, sep=''))
		  }
		  ## Relative Path
		} else {
		  lines <- c(lines, paste('-v ', os_pwd, hostInputDir[[1]][i], ':/', containerInputDir, sep=''))
		}
	  }
	  ## Mount Output Dir
	  if (substr(hostOutputDir, 2, 2) == ':') {
	    ## Root Directory ('C:')
	    if (nchar(hostOutputDir) == 2) {
	      lines <- c(lines, paste('-v ', hostOutputDir, '\\', ':/', containerOutputDir, sep=''))
	    ## Absolute Path
	    } else {
		  lines <- c(lines, paste('-v ', hostOutputDir,':/', containerOutputDir, sep=''))
		}
	  ## Relative Path
	  } else {
		lines <- c(lines, paste('-v ', os_pwd, hostOutputDir,':/',containerOutputDir, sep=''))
	  }
  	  
  	## Linux/Mac  
	} else if (os == 'linux/mac') {
      lines <- c(lines, 'sudo docker run --rm')
	  ## Mount Input Dirs
	  for (i in 1:length(hostInputDir[[1]])){
        if (i > 1) {break} # currently only supports one input directory
		## Absolute Path/Home Path
		if (substr(hostInputDir[[1]][i], 1, 1) == '/' || substr(hostInputDir[[1]][i], 1, 1) == '~') {
			lines <- c(lines, paste('-v ', hostInputDir[[1]][i], ':/', containerInputDir, sep=''))
		## Relative Path
		} else {
		  lines <- c(lines, paste('-v ', os_pwd, hostInputDir[[1]][i], ':/', containerInputDir, sep=''))
		}
	  }
	  ## Mount Output Dir
	  ## Absolute Path/Home Path
	  if (substr(hostOutputDir, 1, 1) == '/' || substr(hostOutputDir, 1, 1) == '~') {
		  lines <- c(lines, paste('-v ', hostOutputDir,':/',containerOutputDir, sep=''))
	  ## Relative Path
	  } else {
		lines <- c(lines, paste('-v ', os_pwd, hostOutputDir,':/',containerOutputDir, sep=''))
	  }
	}
	
	## Docker Image to Run
	lines <- c(lines, dockerhub_address)
	
	## Input Files
	hostInputFilePaths <- list()
	for (i in 1:length(hostInputFileName[[1]])) {
	  hostInputFilePaths <- c(hostInputFilePaths, paste(containerInputDir, hostInputFileName[[1]][i], sep='/'))
	}
	hostInputFilePaths <- paste(hostInputFilePaths, collapse=',')
      
	if (fs == 'fs') {
	  ## nestedboth_montecarlo
	  if (validation == 'mc') {
		lines <- c(lines, '/UserScripts/nestedboth_montecarlo')
		lines <- c(lines, paste('--data', paste("\"", hostInputFilePaths, "\"", sep='')))
		lines <- c(lines, paste('--description', expDesc))
		lines <- c(lines, paste('--outer-iterations', mc_outer))
		lines <- c(lines, paste('--inner-iterations', mc_inner))
		lines <- c(lines, paste('--fs-algo', fsAlgos))
		lines <- c(lines, paste('--classif-algo', paste("\"", classifAlgos, "\"", sep='')))
		lines <- c(lines, paste('--num-features', numFeaturesOptions))
        lines <- c(lines, paste('--output-dir', paste("\"", containerOutputDir, "\"", sep='')))
	  ## nestedboth_crossvalidation  
	  } else if (validation == 'kf') {
		lines <- c(lines, '/UserScripts/nestedboth_crossvalidation')
		lines <- c(lines, paste('--data', paste("\"", hostInputFilePaths, "\"", sep='')))
		lines <- c(lines, paste('--description', expDesc))
		lines <- c(lines, paste('--iterations', kf_iterations))
		lines <- c(lines, paste('--outer-folds', kf_outer))
		lines <- c(lines, paste('--inner-folds', kf_inner))
		lines <- c(lines, paste('--fs-algo', fsAlgos))
		lines <- c(lines, paste('--classif-algo', paste("\"", classifAlgos, "\"", sep='')))
		lines <- c(lines, paste('--num-features', numFeaturesOptions))
        lines <- c(lines, paste('--output-dir', paste("\"", containerOutputDir, "\"", sep='')))
	  }
	} else if (fs == 'no_fs') {
	  ## nestedclassification_montecarlo
	  if (validation == 'mc') {
		lines <- c(lines, '/UserScripts/nestedclassification_montecarlo')
		lines <- c(lines, paste('--data', paste("\"", hostInputFilePaths, "\"", sep='')))
		lines <- c(lines, paste('--description', expDesc))
		lines <- c(lines, paste('--outer-iterations', mc_outer))
		lines <- c(lines, paste('--inner-iterations', mc_inner))
		lines <- c(lines, paste('--classif-algo', paste("\"", classifAlgos, "\"", sep='')))
        lines <- c(lines, paste('--output-dir', paste("\"", containerOutputDir, "\"", sep='')))
	  ## nestedclassification_crossvalidation
	  } else if (validation == 'kf') {
		lines <- c(lines, '/UserScripts/nestedclassification_crossvalidation')
		lines <- c(lines, paste('--data', paste("\"", hostInputFilePaths, "\"", sep='')))
		lines <- c(lines, paste('--description', expDesc))
		lines <- c(lines, paste('--iterations', kf_iterations))
		lines <- c(lines, paste('--outer-folds', kf_outer))
		lines <- c(lines, paste('--inner-folds', kf_inner))
		lines <- c(lines, paste('--classif-algo', paste("\"", classifAlgos, "\"", sep='')))
        lines <- c(lines, paste('--output-dir', paste("\"", containerOutputDir, "\"", sep='')))
	  }
	}
	
	if (is.integer(seed))
	  lines <- c(lines, paste('--seed', seed))
	if (ohe == 'true')
	  lines <- c(lines, paste('--ohe', ohe))
	if (stan == 'true')
	  lines <- c(lines, paste('--standardize', stan))
	if (impute == 'true')
	  lines <- c(lines, paste('--impute', impute))
	
	
	# Linux/Mac use '\' and '\n'
    if (os == 'linux/mac') {
      lines <- paste(lines, collapse=' \\\n  ')
    # Windows: use '^' and '\r\n'
	} else if (os == 'windows') {
	  lines <- paste(lines, collapse=' ^\r\n  ')
    }
    shiny_script <<- lines
  })
  
  output$display_script_ui <- renderUI({
	verbatimTextOutput('shiny_script')
  })

  ## Navigation Buttons
  output$nav_1_ui <- renderUI({
	actionButton('nav_1_to_2_button', 'Next', style="color: #fff; background-color: #337ab7; border-color: #2e6da4")
  })
  observeEvent(input$nav_1_to_2_button, {
	  updateTabsetPanel(session, 'main_panel', selected = '2')
  })
  output$nav_2_ui <- renderUI({
    fluidRow(
	actionButton('nav_2_to_1_button', 'Back'),
	actionButton('nav_2_to_3_button', 'Next',style="color: #fff; background-color: #337ab7; border-color: #2e6da4")
	)
  })
  observeEvent(input$nav_2_to_1_button, {
	  updateTabsetPanel(session, 'main_panel', selected = '1')
  })
  output$nav_2_to_3_button_ui <- renderUI({
	actionButton('nav_2_to_3_button', 'Next',style="color: #fff; background-color: #337ab7; border-color: #2e6da4")
  })
  observeEvent(input$nav_2_to_3_button, {
	  updateTabsetPanel(session, 'main_panel', selected = '3')
  })
  output$nav_3_ui <- renderUI({
    fluidRow(
	actionButton('nav_3_to_2_button', 'Back'),
	actionButton('nav_3_to_4_button', 'Next',style="color: #fff; background-color: #337ab7; border-color: #2e6da4")
	)
  })
  observeEvent(input$nav_3_to_2_button, {
	  updateTabsetPanel(session, 'main_panel', selected = '2')
  })
  output$nav_3_to_4_button_ui <- renderUI({
	actionButton('nav_3_to_4_button', 'Next',style="color: #fff; background-color: #337ab7; border-color: #2e6da4")
  })
  observeEvent(input$nav_3_to_4_button, {
	  updateTabsetPanel(session, 'main_panel', selected = '4')
  })
  output$nav_4_ui <- renderUI({
    fluidRow(
	  actionButton('nav_4_to_3_button', 'Back'),
	  actionButton('nav_4_to_5_button', 'Next',style="color: #fff; background-color: #337ab7; border-color: #2e6da4")
	)
  })
  observeEvent(input$nav_4_to_3_button, {
	  updateTabsetPanel(session, 'main_panel', selected = '3')
  })
  observeEvent(input$nav_4_to_5_button, {
	  updateTabsetPanel(session, 'main_panel', selected = '5')
  })
  output$nav_5_ui <- renderUI({
    fluidRow(
	  actionButton('nav_5_to_4_button', 'Back'),
	  actionButton('nav_5_to_6_button', 'Next',style="color: #fff; background-color: #337ab7; border-color: #2e6da4")
	)
  })
  observeEvent(input$nav_5_to_4_button, {
	  updateTabsetPanel(session, 'main_panel', selected = '4')
  })
  observeEvent(input$nav_5_to_6_button, {
	  updateTabsetPanel(session, 'main_panel', selected = '6')
  })  
  output$nav_6_ui <- renderUI({
    actionButton('nav_6_to_5_button', 'Back')
  })
  observeEvent(input$nav_6_to_5_button, {
	  updateTabsetPanel(session, 'main_panel', selected = '5')
  })

})
