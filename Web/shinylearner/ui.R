library(shiny)

shinyUI(navbarPage(id='navbar', "ShinyLearner",
# Analyze Data
  tabPanel(id='analyze_data','Analyze Data',sidebarLayout(
    sidebarPanel(
      textInput("shared_dir", "Data and Results Directory (relative to host working dir)", value='v'),
      textInput("class_file", "Class File", value='blca_cv_surv1_blca.tsv.gz'),
      textInput("molecular_file", "Molecular Data File", value="mut-ra_blca.tsv.gz"),
      textInput("class_options", "Class Options (comma separated)", value="Short-term Survivor,Long-term Survivor"),
      textInput("exp_name", "Experiment Name", value="Testing BLCA Survival"),
      h4('Script'),
      verbatimTextOutput("shiny_script"),
      actionButton('button_script','Get Script')    
    ),
    mainPanel(
      tags$img(src = "Logo_Big.jpg", width = "484px", height = "374px")
    )
  )),
# Help
  tabPanel(id='help','Help',
    tags$img(src = "Logo_Big.jpg", width = "484px", height = "374px"),
    tags$br(),
    h2('Contact'),
    tags$a(href="http://piccolo.byu.edu/Contact.aspx", target="_blank", "Piccolo Lab at BYU")
  ),
# Contact
  tabPanel(id='contact','Contact',
    tags$img(src = "Logo_Big.jpg", width = "484px", height = "374px"),
    tags$br(),
    h2('Contact'),
    tags$a(href="http://piccolo.byu.edu/Contact.aspx", target="_blank", "Piccolo Lab at BYU")
  )
))
