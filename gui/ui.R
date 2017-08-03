library(shiny)

shinyUI(
  navbarPage(id='navbar', NULL,    
  # Analyze Data
	tabPanel('Analyze Data', id='analyze_data', fluidRow(
	  column(10, offset=1, tags$img(src="Logo_Small.jpg", width='160px', height='124px'), br(), br(), tabsetPanel(id = 'main_panel', type='pills',
		tabPanel("1",br(),
		  # Testing File Input
		  #fileInput('file1', 'Choose File', accept=c('text/plain','.tsv','.csv')),
		  fluidRow(
			column(3, h4('Experiment Description')),
			column(9, uiOutput('exp_desc_help_button_ui'))
		  ),
		  uiOutput('exp_desc_textbox_ui'),
		  uiOutput('exp_desc_help_message_ui'),br(),
		  fluidRow(
			column(3, h4('Input Files')),
			column(9, uiOutput('input_files_help_button_ui'))
		  ),
		  uiOutput('input_files_textbox_ui'),
		  uiOutput('input_files_help_message_ui'),
		  br(),
		  fluidRow(
			column(3, h4('Output Directory')),
			column(9, uiOutput('output_dir_help_button_ui'))
		  ),
		  uiOutput('output_dir_textbox_ui'),
		  uiOutput('output_dir_help_message_ui'),
		  br(),
		  uiOutput('nav_1_ui')
		),
		tabPanel("2",br(),
		  fluidRow(
			column(3, h4('Validation Method')),
			column(9, uiOutput('validation_help_button_ui'))
		  ),
		  uiOutput('validation_radio_ui'),
		  uiOutput('validation_help_message_ui'),
		  br(),
		  fluidRow(
			column(3, h4('Feature Selection')),
			column(9, uiOutput('feat_sel_help_button_ui'))
		  ),
		  uiOutput('feat_sel_radio_ui'),
		  uiOutput('feat_sel_help_message_ui'),br(),br(),
		  uiOutput('nav_2_ui')
		),
		tabPanel("3",br(),
		  fluidRow(
		    column(3, h4('Validation Settings')),
		    column(9, uiOutput('val_settings_help_button_ui'))
		  ),br(),
		  uiOutput('mc_inner_iterations_radio_ui'),
		  uiOutput('mc_outer_iterations_radio_ui'),
		  uiOutput('kf_help_button_ui'),
		  uiOutput('kf_inner_folds_radio_ui'),
		  uiOutput('kf_outer_folds_radio_ui'),
		  uiOutput('kf_iterations_radio_ui'),
          uiOutput('val_settings_help_message_ui'),br(),
		  uiOutput('nav_3_ui')
		),
		tabPanel("4",br(),
		  fluidRow(
			fluidRow(
			  column(4, uiOutput('sel_fsAlgos_header_ui')),
			  column(8, uiOutput('sel_fsAlgos_help_button_ui'))
			),
			uiOutput('sel_fsAlgos_ui'),
			uiOutput('sel_FSOpt_ui'),
			uiOutput('sel_fsAlgos_help_message_ui'),
			fluidRow(
			  column(4, uiOutput('sel_classifAlgos_header_ui')),
			  column(8, uiOutput('sel_classifAlgos_help_button_ui'))
			),
			uiOutput('sel_classifAlgos_ui'),
			uiOutput('sel_classifOpt_ui'),
			uiOutput('sel_classifAlgos_help_message_ui'),br(),br(),
			uiOutput('nav_4_ui')
		  )
		),
		tabPanel("5",br(),
          h4('Additional Options'),
          br(),
		  uiOutput('seed_textbox_ui'),
		  uiOutput('seed_help_message_ui'), br(),
		  uiOutput('ohe_checkbox_ui'),
		  uiOutput('ohe_help_message_ui'),
		  uiOutput('stan_checkbox_ui'),
		  uiOutput('stan_help_message_ui'),
		  uiOutput('impute_checkbox_ui'),
		  uiOutput('impute_help_message_ui'),
          br(),
		  uiOutput('nav_5_ui')
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
			tags$li(HTML('Install and Start <a target=_blank href=http://www.docker.com>Docker</a>.')),
			tags$li('Open Terminal (Mac/Linux) or Command Prompt (Windows).'),
			tags$li('Navigate to the directory containing "Input Files" and "Output Directory".'),
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
)

# old code for putting logo inside the navbar
#fluidPage(
  #div(titlePanel(title="", windowTitle="ShinyLearner")),tags$style(".navbar {height: 100px; font-size:100%;}"),
  #navbarPage(id='navbar', img(src="Logo_Small.jpg", width="90px", height="75px"),
  # rest of code here
  #...................
  #)
#)