library(shiny)

shinyUI(fluidPage(
  tags$head(tags$style(HTML("custom-help-block {color: red; }"))),
  navbarPage(id='navbar', NULL,    
  # Analyze Data
	tabPanel('Analyze data', id='analyze_data', fluidRow(
	  column(10, offset=1, tags$img(src="Logo_Small.jpg", width='160px', height='124px'), br(), br(), tabsetPanel(id = 'main_panel', type='pills',
		tabPanel("1",br(),
		  fluidRow(column(3, h4('Experiment description (required):'))),
		  uiOutput('exp_desc_textbox_ui'),
		  uiOutput('exp_desc_help_message_ui'),br(),

			fluidRow(column(3, h4('Input data directory (required):'))),
			uiOutput('input_dir_textbox_ui'),
			uiOutput('input_dir_help_message_ui'),
			br(),

		  fluidRow(column(3, h4('Input files (required):'))),
		  uiOutput('input_files_textbox_ui'),
		  uiOutput('input_files_help_message_ui'),
		  br(),

		  fluidRow(column(3, h4('Output directory (required):'))),
		  uiOutput('output_dir_textbox_ui'),
		  uiOutput('output_dir_help_message_ui'),
		  br(),
		  uiOutput('nav_1_ui'),br()
		),
		tabPanel("2",br(),
		         h4('Data preprocessing options:'),
		         uiOutput('ohe_checkbox_ui'),
		         uiOutput('ohe_help_message_ui'),
		         uiOutput('scale_dropdown_ui'),
		         uiOutput('scale_help_message_ui'),
		         uiOutput('impute_checkbox_ui'),
		         uiOutput('impute_help_message_ui'),
		         br(),
		         uiOutput('nav_2_ui'),br()
		),
		tabPanel("3",br(),
		  fluidRow(column(3, h4('Validation method:'))),
		  uiOutput('validation_radio_ui'),
		  uiOutput('validation_help_message_ui'),
		  br(),
		  fluidRow(column(3, h4('Feature selection:'))),
		  uiOutput('feat_sel_radio_ui'),
		  uiOutput('feat_sel_help_message_ui'),br(),br(),
		  uiOutput('nav_3_ui'),br()
		),
		tabPanel("4",br(),
		         fluidRow(
		           fluidRow(column(4, uiOutput('sel_classifAlgos_header_ui'))),
		           uiOutput('sel_classifAlgos_ui'),
		           uiOutput('sel_classifOpt_ui'),
		           uiOutput('sel_gpu_ui'),
		           uiOutput('sel_classifAlgos_help_message_ui'),
		           fluidRow(column(4, uiOutput('sel_fsAlgos_header_ui'))),
		           uiOutput('sel_fsAlgos_ui'),
		           uiOutput('sel_fsAlgos_help_message_ui'),
		           br(),br(),
		           uiOutput('nav_4_ui'),br()
		         )
		),
		tabPanel("5",br(),
		         fluidRow(column(3, h4('Validation settings:'))),br(),
		         uiOutput('mc_inner_iterations_radio_ui'),
		         uiOutput('mc_outer_iterations_radio_ui'),
		         uiOutput('kf_inner_folds_radio_ui'),
		         uiOutput('kf_outer_folds_radio_ui'),
		         uiOutput('val_settings_help_message_ui'),
		         uiOutput('kf_iterations_radio_ui'),
		         uiOutput('val_settings_iterations_help_message_ui'),
		         br(),
		         uiOutput('seed_textbox_ui'),
		         uiOutput('seed_help_message_ui'),
		         br(),
		         uiOutput('nav_5_ui'),br()
		),
		tabPanel("6",br(),
		  fluidRow(column(3, h4('Operating System:'))),
		  uiOutput('os_ui'),
		  uiOutput('os_help_message_ui'),br(),
		  h4('Instructions:'),
		  tags$ol(
			tags$li(HTML('Install and start the  <a target=_blank href=http://www.docker.com>Docker</a> software.')),
			tags$li('Open Terminal (Mac/Linux) or Command Prompt (Windows).'),
			tags$li(HTML('Copy and paste the command below in the Terminal/Command window and hit Enter. (Alternatively, you can create a <a target="_blank" href="https://www.taniarascia.com/how-to-create-and-use-bash-scripts/">bash script</a> and execute that.)'))
		  ),br(),
          h4('Command:'),
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
		h3('Contact'),br(),
		tags$ul(
		  tags$li(tags$a(href="http://piccolo.byu.edu/Contact.aspx", target="_blank", "Piccolo Lab at BYU")),br(),
		  tags$li(tags$a(href="https://github.com/srp33/ShinyLearner", target="_blank", "Github site")),br(),
		  tags$li(tags$a(href="https://github.com/srp33/ShinyLearner/issues", target="_blank", "Submit bug report"))
		)
	  ),
	  column(1)
	  )
	)
  )
))
