library(shiny)

shinyUI(fluidPage(
  tags$head(tags$style(HTML("custom-help-block {color: red; }"))),
  navbarPage(id='navbar', NULL,    
  # Analyze Data
	tabPanel('Analyze data', id='analyze_data', fluidRow(
	  column(10, offset=1, tags$img(src="Logo_Small.jpg", width='160px', height='124px'), br(), br(), tabsetPanel(id = 'main_panel', type='pills',
		tabPanel("1",br(),
		  # Testing File Input
		  #fileInput('file1', 'Choose File', accept=c('text/plain','.tsv','.csv')),
		  fluidRow(
			column(3, h4('Experiment description (required)')),
			column(9, uiOutput('exp_desc_help_button_ui'))
		  ),
		  uiOutput('exp_desc_textbox_ui'),
		  uiOutput('exp_desc_help_message_ui'),br(),
		  fluidRow(
			column(3, h4('Input files (required)')),
			column(9, uiOutput('input_files_help_button_ui'))
		  ),
		  uiOutput('input_files_textbox_ui'),
		  uiOutput('input_files_help_message_ui'),
		  br(),
		  fluidRow(
			column(3, h4('Output directory (required)')),
			column(9, uiOutput('output_dir_help_button_ui'))
		  ),
		  uiOutput('output_dir_textbox_ui'),
		  uiOutput('output_dir_help_message_ui'),
		  br(),
		  uiOutput('nav_1_ui'),br()
		),
		tabPanel("2",br(),
		  fluidRow(
			column(3, h4('Validation method')),
			column(9, uiOutput('validation_help_button_ui'))
		  ),
		  uiOutput('validation_radio_ui'),
		  uiOutput('validation_help_message_ui'),
		  br(),
		  fluidRow(
			column(3, h4('Feature selection')),
			column(9, uiOutput('feat_sel_help_button_ui'))
		  ),
		  uiOutput('feat_sel_radio_ui'),
		  uiOutput('feat_sel_help_message_ui'),br(),br(),
		  uiOutput('nav_2_ui'),br()
		),
		tabPanel("3",br(),
		  fluidRow(
		    column(3, h4('Validation settings')),
		    column(9, uiOutput('val_settings_help_button_ui'))
		  ),br(),
		  uiOutput('mc_inner_iterations_radio_ui'),
		  uiOutput('mc_outer_iterations_radio_ui'),
		  uiOutput('kf_help_button_ui'),
		  uiOutput('kf_inner_folds_radio_ui'),
		  uiOutput('kf_outer_folds_radio_ui'),
		  uiOutput('kf_iterations_radio_ui'),
          uiOutput('val_settings_help_message_ui'),
          br(),
		  uiOutput('nav_3_ui'),br()
		),
		tabPanel("4",br(),
		  fluidRow(

			fluidRow(
			  column(4, uiOutput('sel_classifAlgos_header_ui')),
			  column(8, uiOutput('sel_classifAlgos_help_button_ui'))
			),
			uiOutput('sel_classifAlgos_ui'),
			uiOutput('sel_classifOpt_ui'),
			uiOutput('sel_classifAlgos_help_message_ui'),
			fluidRow(
			  column(4, uiOutput('sel_fsAlgos_header_ui')),
			  column(8, uiOutput('sel_fsAlgos_help_button_ui'))
			),
			uiOutput('sel_fsAlgos_ui'),
			uiOutput('sel_fsAlgos_help_message_ui'),
            br(),br(),
			uiOutput('nav_4_ui'),br()
		  )
		),
		tabPanel("5",br(),
          h4('Additional options'),
          br(),
		  uiOutput('ohe_checkbox_ui'),
		  uiOutput('ohe_help_message_ui'),
		  uiOutput('scale_checkbox_ui'),
		  uiOutput('scale_help_message_ui'),
		  uiOutput('impute_checkbox_ui'),
		  uiOutput('impute_help_message_ui'),
          br(),
		  uiOutput('seed_textbox_ui'),
		  uiOutput('seed_help_message_ui'),
          br(),
		  uiOutput('nav_5_ui'),br()
		),
		tabPanel("6",br(),
		  fluidRow(
			column(3, h4('Operating System')),
			column(9, uiOutput('os_help_button_ui'))
		  ),
		  uiOutput('os_ui'),
		  uiOutput('os_help_message_ui'),br(),
		  h4('Instructions'),
		  tags$ol(
			tags$li(HTML('Install and start <a target=_blank href=http://www.docker.com>Docker</a>.')),
			tags$li('Open Terminal (Mac/Linux) or Command Prompt (Windows).'),
			tags$li('Copy and paste the command below.')
		  ),br(),
          h4('Command'),
		  uiOutput('display_script_ui'),br(),br(),
		  uiOutput('nav_6_ui'),br()
		)
	  )),
	  column(1)
	  )
	),
  # Contact
	tabPanel(id='contact','Contact', fluidRow(
	  column(10, offset=1,
		tags$img(src="Logo_Small.jpg", width='160px', height='124px'), br(),br(),
		h3('Contact'),br(),br(),
		tags$ul(
		  tags$li(tags$a(href="http://piccolo.byu.edu/Contact.aspx", target="_blank", "Piccolo Lab at BYU")),br(),
		  tags$li(tags$a(href="https://github.com/srp33/ShinyLearner", target="_blank", "ShinyLearner on Github"))
		),br(),br(),
		tags$i("Please submit bug reports to the Github page.")
	  ),
	  column(1)
	  )
	)
  )
))

# old code for putting logo inside the navbar
#fluidPage(
  #div(titlePanel(title="", windowTitle="ShinyLearner")),tags$style(".navbar {height: 100px; font-size:100%;}"),
  #navbarPage(id='navbar', img(src="Logo_Small.jpg", width="90px", height="75px"),
  # rest of code here
  #...................
  #)
#)
