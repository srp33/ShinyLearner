############################################################
############################################################
# Edit server_template.R rather than server.R.
############################################################
############################################################

library(shiny)

shinyServer(function(input, output, session) {
  
  session$allowReconnect(TRUE)
  docker_image_name <- 'srp33/shinylearner'
  docker_image_tag <- 'version587'
  numFeaturesOptions <- '1,10,100,1000,10000'
  defaultValidation <- 'mc'
  validationChoices <- list('Monte Carlo cross validation' = 'mc', 'k-fold cross validation' = 'kf')
  defaultFS <- 'no_fs'
  defaultInnerIterations <- 5
  mc_inner_options <- list(1,5,10,50,100)
  defaultOuterIterations <- 10
  mc_outer_options <- list(1,5,10,50,100)
  defaultInnerFolds <- 5
  kf_inner_options <- list(2, 3, 5,10)
  defaultOuterFolds <- 10
  kf_outer_options <- list(2, 3, 5,10)
  defaultIterations <- 1
  kf_iterations_options <- list(1,5,10,50,100)
  defaultOS <- 'linux/mac'
  osOptions <- list('Linux or Mac' = 'linux/mac', 'Windows' = 'windows')
  defaultFSAlgos <- 'AlgorithmScripts/FeatureSelection/tsv/sklearn/anova'
  defaultClassifAlgos <- 'AlgorithmScripts/Classification/tsv/sklearn/svm'
  defaultClassifOpt <- FALSE
  defaultGPUOpt <- FALSE
  defaultOHE <- TRUE
  defaultScale <- 'robust'
  defaultImpute <- FALSE
  defaultSeed <- 1
  containerInputDir <- '/InputData'
  containerOutputDir <- '/OutputData'
  
  helpTextStylingOpen <- '<p style="color:rgb(128,128,128)">'
  helpTextStylingClose <- '</p>'
  errorTextStylingOpen <- '<p style="color:rgb(256,0,0)">'
  errorTextStylingClose <- '</p>'
  exp_desc_help_text <- 'Please enter a short, unique description of the analysis. This descriptor will be included in the output files so you can uniquely identify this analysis. (Avoid using space characters in this description ShinyLearner will replace spaces with underscore characters.)'
  input_dir_help_text <- 'Please indicate the directory on your computer where the data files that you want to analyze are stored. Please use an <a target="_blank" href="https://en.wikipedia.org/wiki/Path_(computing)">absolute file path</a>.'
  input_files_help_text <- 'Please indicate the name(s) of the data files that you would like to analyze. The files should be present in the "Input data directory" specified above. Files can also be present in a subdirectory of the input data directory; in this case, use relative paths. <a target=_blank" href="https://github.com/srp33/ShinyLearner/blob/master/InputFormats.md">This page</a> explains the supported file formats. You can specify multiple files by separating the file names with commas. Wildcards are also allowed (for example, *.csv). When multiple file names have been specified, ShinyLearner will merge them.'
  output_dir_help_text <- 'Please specify a directory on your computer where the output files will be stored after ShinyLearner has completed the analysis. Please use an <a target="_blank" href="https://en.wikipedia.org/wiki/Path_(computing)">absolute file path</a>. Text files that contain the results of the analysis will be created in this directory.'
  validation_help_text <- 'An important aspect of supervised machine learning is to assess how well the algorithmic predictions will generalize (make successful predictions on new data). ShinyLearner supports two ways of assessing generalizability: Monte Carlo cross validation and k-fold cross validation. You can read more about these methods <a target="_blank" href="https://en.wikipedia.org/wiki/Cross-validation_(statistics)">here</a>. The Monte Carlo method randomly assigns samples to training and testing sets and repeats this process for many iterations. The k-fold method assigns samples to training and testing sets such that each sample is tested exactly once per iteration. (You can also execute multiple iterations of k-fold cross validation.)'
  feat_sel_help_text <- 'Feature selection algorithms seek to identify features (independent variables) that are most informative. Oftentimes, reducing the size of the data via feature selection leads to higher accuracy. Feature selection may also make it easier for a human to understand which parts of the data are most important. However, feature selection does increase the computer-execution time.'
  sel_classifAlgos_help_text <- 'Choose one or more classification algorithms. ShinyLearner supports a wide variety of algorithms from popular machine-learning libraries. You can learn more about these algorithms <a target="_blank" href="https://github.com/srp33/ShinyLearner/blob/master/Algorithms.md">here</a>. (Please let us know if you would like us to support additional algorithms or hyperparameters). When "Optimize hyperparameters" is selected, all hyperparameter combinations currently supported in ShinyLearner will be used for optimization; this will increase runtimes considerably, but it may increase accuracy, too.'
  sel_fsAlgos_help_text <- 'Choose one or more feature-selection algorithms. ShinyLearner has integrated a wide variety of algorithms from popular machine-learning libraries. You can learn more about these algorithms <a target="_blank" href="https://github.com/srp33/ShinyLearner/blob/master/Algorithms.md">here</a>.'
  os_help_text <- 'ShinyLearner will be executed within a "software container" (explanation <a target="_blank" href="https://gigascience.biomedcentral.com/articles/10.1186/s13742-016-0135-4">here</a>) using the <a target="_blank" href="https://www.docker.com">Docker</a> technology. Docker can be executed on many operating systems, including Mac OS, Windows, and Linux. But the command that you use to execute Docker may be different, depending on the operating system.'
  mc_help_text <- 'Monte Carlo cross validation is typically executed in multiple iterations. This helps with estimating the consistency of an algorithm\'s performance. In each iteration, a different training and test set is selected randomly from the full data set. A larger number of iterations should lead to more robust results but will also increase computational time.'
  kf_help_text <- 'This setting allows you to select a value for <em>k</em> when performing k-fold cross-validation. Higher <em>k</em> values result in a larger number of training and test sets but also increases computational time.'
  kf_iterations_help_text <- 'You may also indicate the number of times that k-fold cross validation should be repeated. Different training and test sets will be selected randomly for each iteration.'
  mc_nested_help_text <- 'Monte Carlo cross validation is typically executed in multiple "outer" iterations. This helps with estimating the consistency of an algorithm\'s performance. In each "outer" iteration, a different training and test set is selected randomly from the full data set. A larger number of "outer" iterations should lead to more robust results but also increases computational time. When using multiple algorithms, optimizing hyperparameters, or performing feature selection, you need a way to select from among these options. The "inner" iterations allow you to break each training set into sub-training and sub-test tests and try various options (e.g., parameters, features). A larger number of "inner" iterations should lead to better selections but also increases computational time.'
  kf_nested_help_text <- 'These settings allow you to select values for <em>k</em> when performing k-fold cross-validation. Higher <em>k</em> values result in a larger number of training and test sets but also increases computational time. When using multiple algorithms, optimizing hyperparameters, or performing feature selection, you need a way to select from among these options. The "inner" folds allow you to break each training set into sub-training and sub-test tests and try various options (e.g., parameters, features). A larger number of "inner" folds should lead to better selections but will also increase computational time.'
  kf_nested_iterations_help_text <- 'You may also indicate the number of times that k-fold cross validation should be repeated. Different training and test sets will be selected randomly for each outer and inner fold.'
  ohe_help_text <- 'Many machine-learning algorithms are unable to process discrete variables, so one-hot encoding can be used to expand discrete variables into multiple binary variables. You can learn more about this option <a target="_blank" href="https://www.quora.com/What-is-one-hot-encoding-and-when-is-it-used-in-data-science">here</a>.'
  scale_help_text <- 'Many machine-learning algorithms require that continuous variables be scaled to ensure that the algorithms evaluate the variables consistently. ShinyLearner can scale data using one of several methods (<a target="_blank" href="https://scikit-learn.org/stable/auto_examples/preprocessing/plot_all_scaling.html#sphx-glr-auto-examples-preprocessing-plot-all-scaling-py">described here</a>).'
  impute_help_text <- 'Many machine-learning algorithms are unable to process missing data values. This option makes it possible to <a target="_blank" href="https://en.wikipedia.org/wiki/Imputation_(statistics)">impute</a> missing values. Median-based imputation is used for continuous and integer variables. Mode-based imputation is used for discrete variables. Any variable missing more than 50% of values across all samples will be removed. Subsequently, any sample missing more than 50% of values across all features will be removed. In input data files, missing values should be specified as ?, NA, or null.'
  seed_help_text <- 'When samples are assigned to training and testing sets, they are randomly assigned. To ensure that samples are assigned in a consistent manner when the same analysis is repeated, we use a random seed. ShinyLearner sets the seed by default, but you can change the seed using this option. Please specify an integer. Note: some machine-learning algorithms non-deterministic, so they may produce different results each time they are run, even when a seed is specified.'
  incomplete_error_message <- "Please complete the other tabs before proceeding."
  
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
  
  ## Experiment Description
  output$exp_desc_textbox_ui <-renderUI({
    textInput("exp_desc_textbox", NULL, value="", width='100%')
  })
  output$exp_desc_help_message_ui <- renderUI({
    HTML(paste(helpTextStylingOpen, exp_desc_help_text, helpTextStylingClose, sep=''))
  })
  ## Input Dir
  output$input_dir_textbox_ui <-renderUI({
    textInput("input_dir_textbox", NULL, value="", width='100%')
  })
  output$input_dir_help_message_ui <- renderUI({
    HTML(paste(helpTextStylingOpen, input_dir_help_text, helpTextStylingClose, sep=''))
  })
  ## Input Files
  output$input_files_textbox_ui <-renderUI({
    textInput("input_files_textbox", NULL, value="", width='100%')
  })
  ## Input Files Help
  output$input_files_help_message_ui <- renderUI({
    HTML(paste(helpTextStylingOpen, input_files_help_text, helpTextStylingClose, sep=''))
  })
  ## Output Directory
  output$output_dir_textbox_ui <-renderUI({
    textInput("output_dir_textbox", NULL, value="", width='100%')
  })
  ## Output Files Help
  output$output_dir_help_message_ui <- renderUI({
    HTML(paste(helpTextStylingOpen, output_dir_help_text, helpTextStylingClose, sep=''))
  })
  
  ## Choose Validation UI
  output$validation_radio_ui <- renderUI({
    radioButtons('validation_radio', NULL, validationChoices, selected=defaultValidation)
  })
  output$validation_help_message_ui <- renderUI({
    HTML(paste(helpTextStylingOpen, validation_help_text, helpTextStylingClose, sep=''))
  })
  ## Choose Feature Selection UI
  output$feat_sel_radio_ui <- renderUI({
    radioButtons('feat_sel_radio', NULL, list('Yes' = 'fs', 'No' = 'no_fs'), selected=defaultFS)
  })
  output$feat_sel_help_message_ui <- renderUI({
    HTML(paste(helpTextStylingOpen, feat_sel_help_text, helpTextStylingClose, sep=''))
  })

  is_validation_set <- function() {length(input$validation_radio) != 0}
  is_monte_carlo <- function() {input$validation_radio == 'mc'}
  is_k_fold <- function() {input$validation_radio == 'kf'}
  is_nested_validation <- function() {
    length(input$sel_classifAlgos) > 1 || 
    input$feat_sel_radio == 'fs' ||
    (!is.null(input$sel_classifOpt) && input$sel_classifOpt)
  }
  
  ## MC Inner Iterations
  output$mc_inner_iterations_radio_ui <- renderUI({ 
    if (is_validation_set() && is_monte_carlo() && is_nested_validation()) {
      radioButtons('mc_inner_iterations_radio', HTML('Choose the number of <em>inner</em> Monte Carlo iterations:'), mc_inner_options, selected = defaultInnerIterations)
    }
  })
  ## MC Outer Iterations
  output$mc_outer_iterations_radio_ui <- renderUI({
    if (is_validation_set()) {
      if (is_monte_carlo()) {
        message <- ifelse(is_nested_validation(), 'Choose the number of <i>outer</i> Monte Carlo iterations:', "Choose the number of Monte Carlo iterations:")
        radioButtons('mc_outer_iterations_radio', HTML(message), mc_outer_options, selected=defaultOuterIterations)
      }
    } else {
      HTML(paste0(errorTextStylingOpen, incomplete_error_message, errorTextStylingClose))
    }
  })
  ## KF Inner Folds
  output$kf_inner_folds_radio_ui <- renderUI({
    if (is_validation_set() && is_k_fold() && is_nested_validation())
      radioButtons('kf_inner_folds_radio', HTML('Choose the number of <em>inner</em> folds for k-fold cross validation:'), kf_inner_options, selected=defaultInnerFolds)
  })
  ## KF Outer Folds
  output$kf_outer_folds_radio_ui <- renderUI({
    if (is_validation_set()) {
      if (is_k_fold()) {
        message <- ifelse(is_nested_validation(), 'Choose the number of <em>outer</em> folds for k-fold cross validation:', 'Choose number of folds for k-fold cross validation:')
        radioButtons('kf_outer_folds_radio', HTML(message), kf_outer_options, selected=defaultOuterFolds)
      }
    }
  })
  ## KF Iterations
  output$kf_iterations_radio_ui <- renderUI({
    if (is_validation_set() && is_k_fold())
      radioButtons('kf_iterations_radio', HTML('Choose the number of iterations:'), kf_iterations_options, selected=defaultIterations)
  })
  output$val_settings_help_message_ui <- renderUI({
    if (is_validation_set()) {
      if (is_monte_carlo()) {
        if (is_nested_validation()) {
          HTML(paste(helpTextStylingOpen, mc_nested_help_text, helpTextStylingClose, sep=''))
        } else {
          HTML(paste(helpTextStylingOpen, mc_help_text, helpTextStylingClose, sep=''))
        }
      } else {
        if (is_nested_validation()) {
          HTML(paste(helpTextStylingOpen, kf_nested_help_text, helpTextStylingClose, sep=''))
        } else {
          HTML(paste(helpTextStylingOpen, kf_help_text, helpTextStylingClose, sep=''))
        }
      }
    }
  })
  output$val_settings_iterations_help_message_ui <- renderUI({
    if (is_validation_set()) {
      if (!is_monte_carlo()) {
        if (is_nested_validation()) {
          HTML(paste(helpTextStylingOpen, kf_nested_iterations_help_text, helpTextStylingClose, sep=''))
        } else {
          HTML(paste(helpTextStylingOpen, kf_iterations_help_text, helpTextStylingClose, sep=''))
        }
      }
    }
  })
  
  ## Classification Algorithm
  output$sel_classifAlgos_ui <- renderUI({
    selectizeInput('sel_classifAlgos', NULL, choices = classifAlgosOptions, multiple = TRUE, selected=defaultClassifAlgos)
  })
  output$sel_classifOpt_ui <- renderUI({
    checkboxInput('sel_classifOpt', 'Optimize hyperparameters?', value = defaultClassifOpt)
  })
  output$sel_gpu_ui <- renderUI({
    if (!is.null(input$sel_classifAlgos) & any(grepl("keras", input$sel_classifAlgos))) {
      checkboxInput('sel_gpuOpt', 'Execute on GPUs (where possible)?', value = defaultGPUOpt)
    }
  })
  output$sel_classifAlgos_header_ui <- renderUI({
    h4('Classification algorithms (required)')
  })
  output$sel_classifAlgos_help_message_ui <- renderUI({
    HTML(paste(helpTextStylingOpen, sel_classifAlgos_help_text, helpTextStylingClose, sep=''))
  })
  output$sel_fsAlgos_ui <- renderUI({
    if (length(input$feat_sel_radio) != 0 && input$feat_sel_radio == 'fs') {
      selectizeInput('sel_fsAlgos', NULL, choices = fsAlgosOptions, multiple = TRUE, selected=defaultFSAlgos)
    } else {return()}
  })
  output$sel_fsAlgos_header_ui <- renderUI({
    if (length(input$feat_sel_radio) != 0 && input$feat_sel_radio == 'fs') {
      h4('Feature-selection algorithms (required)')
    } else {return()}
  })
  output$sel_fsAlgos_help_message_ui <- renderUI({
    if (length(input$feat_sel_radio) != 0 && input$feat_sel_radio == 'fs') {
      HTML(paste(helpTextStylingOpen, sel_fsAlgos_help_text, helpTextStylingClose, sep=''))
    } else {return()}
  })
  
  ## One-Hot-Encoding
  output$ohe_checkbox_ui <- renderUI({
    checkboxInput('ohe_checkbox', HTML('<b>One-hot encoding</b>'), value = defaultOHE)
  })
  output$ohe_help_message_ui <- renderUI({
    HTML(paste(helpTextStylingOpen, ohe_help_text, helpTextStylingClose, sep=''))
  })
  ## Scale Data
  output$scale_dropdown_ui <- renderUI({
    choices = c("None"="none", "StandardScaler (center and scale to unit variance)"="standard", "RobustScaler (center and scale based on percentiles)"="robust", "MinMaxScaler (scale to the range [0, 1])"="minmax", "MaxAbsScaler (scale absolute values to the range [0, 1])"="maxabs", "PowerTransformer (scale to a Gaussian distribution using a power transformation)"="power", "QuantNorm (scale to a Gaussian distribution using quantiles)"="quantnorm", "QuantUnif (scale to the range [0, 1] using quantiles)"="quantunif", "Normalizer (rescale each sample)"="normalizer")
    selectInput('scale_dropdown', HTML('<b>Scale data</b>'), choices=choices, selected = defaultScale, selectize=FALSE)
  })
  output$scale_help_message_ui <- renderUI({
    HTML(paste(helpTextStylingOpen, scale_help_text, helpTextStylingClose, sep=''))
  })
  ## Impute Data
  output$impute_checkbox_ui <- renderUI({
    checkboxInput('impute_checkbox', HTML('<b>Impute missing data</b>'), value = defaultImpute)
  })
  output$impute_help_message_ui <- renderUI({
    HTML(paste(helpTextStylingOpen, impute_help_text, helpTextStylingClose, sep=''))
  })
  ## Set Random Seed
  output$seed_textbox_ui <- renderUI({
    textInput('seed_textbox', 'Random seed (integers only)', value = as.character(defaultSeed), placeholder='[Leave blank for default seed]')
  })
  output$seed_help_message_ui <- renderUI({
    HTML(paste(helpTextStylingOpen, seed_help_text, helpTextStylingClose, sep=''))
  })
  
  ## Operating System
  output$os_ui <- renderUI({
    radioButtons('os_radio', NULL, osOptions, selected=defaultOS)
  })
  output$os_help_message_ui <- renderUI({
    HTML(paste(helpTextStylingOpen, os_help_text, helpTextStylingClose, sep=''))
  })

  ## This function synthesizes all of the user's input, and assigns the resulting string to the variable 'shiny_script'.
  output$shiny_script <- renderText({
    
    # Validate required fields (we only need to check one per page - and some pages don't need to be checked)
    validate(need(input$exp_desc_textbox != "" &
                    input$input_dir_textbox != "" &
                    input$input_files_textbox != "" &
                    input$output_dir_textbox != "" &
                    !is.null(input$ohe_checkbox) &
                    !is.null(input$sel_classifOpt) &
                    input$seed_textbox != '',
                  incomplete_error_message))
    
    tilde_error_message <- "The ~ character is not allowed in the input or output directory path. Please use absolute paths."
    validate(need(!grepl("~", input$input_dir_textbox), tilde_error_message))
    validate(need(!grepl("~", input$output_dir_textbox), tilde_error_message))
    validate(need(!is.na(as.integer(input$seed_textbox)), "The random seed must be an integer."))

    ## Get user-specified options
    expDesc <- gsub(' ', '_', input$exp_desc_textbox)
    clientInputDir <- input$input_dir_textbox
    clientInputFiles <- strsplit(input$input_files_textbox, ',')[[1]]
    clientOutputDir <- input$output_dir_textbox
    
    ## Trim trailing '/'
    if (substr(clientInputDir, nchar(clientInputDir), nchar(clientInputDir)) == '/') {
      clientInputDir <- substr(clientInputDir, 0, nchar(clientInputDir)-1)
    }
    if (substr(clientOutputDir, nchar(clientOutputDir), nchar(clientOutputDir)) == '/') {
      clientOutputDir <- substr(clientOutputDir, 0, nchar(clientOutputDir)-1)
    }

    validation <- ifelse(length(input$validation_radio) != 0, input$validation_radio, defaultValidation)
    fs <- ifelse(length(input$feat_sel_radio) != 0, input$feat_sel_radio, defaultFS)
    mc_outer <- ifelse(length(input$mc_outer_iterations_radio) != 0, input$mc_outer_iterations_radio, defaultOuterIterations)
    mc_inner <- ifelse(length(input$mc_inner_iterations_radio) != 0, input$mc_inner_iterations_radio, defaultInnerIterations)
    kf_iterations <- ifelse(length(input$kf_iterations_radio) != 0, input$kf_iterations_radio, defaultIterations)
    kf_outer <- ifelse(length(input$kf_outer_folds_radio) != 0, input$kf_outer_folds_radio, defaultOuterFolds)
    kf_inner <- ifelse(length(input$kf_inner_folds_radio) != 0, input$kf_inner_folds_radio, defaultInnerFolds)

    validate(need(length(input$sel_classifAlgos) > 0, "At least one classification algorithm must be selected."))
    
    if (fs != defaultFS)
      validate(need(length(input$sel_fsAlgos) > 0, "At least one feature-selection algorithm must be selected."))
    
    algo_suffix <- ifelse(input$sel_classifOpt, '/*', '/default*')
    fsAlgos <- paste0("/", input$sel_fsAlgos, algo_suffix)
    classifAlgos <- paste0("/", input$sel_classifAlgos, algo_suffix)
    
    ohe <- ifelse(input$ohe_checkbox, 'true', 'false')
    scale <- ifelse(is.null(input$scale_dropdown), 'none', input$scale_dropdown)
    impute <- ifelse(input$impute_checkbox, 'true', 'false')
    seed <- ifelse(is.null(input$seed_textbox), defaultSeed, as.integer(input$seed_textbox))

    if(length(input$os_radio) != 0)
      os <- input$os_radio
    
    if (os == 'linux/mac') {
      shiny_script <- paste0('mkdir -p "', clientInputDir, '"', getLineEnding(os), getLineEnding(os))
    } else {
      shiny_script <- paste0('if not exist "', clientInputDir, '" mkdir "', clientInputDir, '"', getLineEnding(os), getLineEnding(os))
    }
    lines <- c(lines, '')

    lines <- list()
    lines <- c(lines, 'docker run --rm -i')
    lines <- c(lines, paste0('  -v "', clientInputDir, '":"', containerInputDir, '"'))
    lines <- c(lines, paste0('  -v "', clientOutputDir, '":"', containerOutputDir, '"'))
    
    if (os == 'linux/mac')
      lines <- c(lines, "  --user $(id -u):$(id -g)")
    
    if (!is.null(input$sel_gpuOpt))
      docker_image_name <- ifelse(input$sel_gpuOpt, paste0(docker_image_name, "_gpu"), docker_image_name)
    lines <- c(lines, paste0("  ", docker_image_name, ":", docker_image_tag))
    
    data_line <- paste0('    --data "', clientInputFiles, '"')
    desc_line <- paste0('    --description "', expDesc, '"')
    outer_iter_line <- paste('    --outer-iterations', mc_outer)
    inner_iter_line <- paste('    --inner-iterations', mc_inner)
    iter_line <- paste('    --iterations', mc_outer)
    outer_folds_line <- paste('    --outer-folds', kf_outer)
    inner_folds_line <- paste('    --inner-folds', kf_inner)
    kf_folds_line <- paste('    --folds', kf_outer)
    kf_iter_line <- paste('    --iterations', kf_iterations)
    fs_algo_line <- paste0('    --fs-algo "', fsAlgos, '"')
    classif_algo_line <- paste0('    --classif-algo "', classifAlgos, '"')
    num_features_line <- paste('    --num-features', numFeaturesOptions)

    if (fs == 'fs') {
      if (validation == 'mc') {
        lines <- c(lines, '  /UserScripts/nestedboth_montecarlo')
        lines <- c(lines, data_line, desc_line)
        lines <- c(lines, outer_iter_line, inner_iter_line, fs_algo_line, classif_algo_line, num_features_line)
      } else {
        lines <- c(lines, '  /UserScripts/nestedboth_crossvalidation')
        lines <- c(lines, data_line, desc_line)
        lines <- c(lines, iter_line, outer_folds_line, inner_folds_line, fs_algo_line, classif_algo_line, num_features_line)
      }
    } else {
      if (validation == 'mc') {
        if (is_nested_validation()) {
          lines <- c(lines, '  /UserScripts/nestedclassification_montecarlo')
          lines <- c(lines, data_line, desc_line)
          lines <- c(lines, outer_iter_line, inner_iter_line, classif_algo_line)
        } else {
          lines <- c(lines, '  /UserScripts/classification_montecarlo')
          lines <- c(lines, data_line, desc_line)
          lines <- c(lines, iter_line, classif_algo_line)
        }
      } else {
        if (is_nested_validation()) {
          lines <- c(lines, '  /UserScripts/nestedclassification_crossvalidation')
          lines <- c(lines, data_line, desc_line)
          lines <- c(lines, kf_iter_line, outer_folds_line, inner_folds_line, classif_algo_line)
        } else {
          lines <- c(lines, '  /UserScripts/classification_crossvalidation')
          lines <- c(lines, data_line, desc_line)
          lines <- c(lines, kf_iter_line, kf_folds_line, classif_algo_line)
        }
      }
    }

    lines <- c(lines, paste('    --seed', seed))
    lines <- c(lines, paste('    --ohe', ohe))
    lines <- c(lines, paste('    --scale', scale))
    lines <- c(lines, paste('    --impute', impute))
    
    shiny_script <- paste0(shiny_script, paste(lines, collapse=paste0(getLineContinuation(os), getLineEnding(os))))
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

getLineContinuation <- function(os) {
  if (os == 'linux/mac') {
    return(' \\')
  } else {
    return(' ^')
  }
}

getLineEnding <- function(os) {
  if (os == 'linux/mac') {
    return('\n')
  } else {
    return('\r\n')
  }
}
