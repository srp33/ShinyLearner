FROM rocker/shiny:latest

ADD server.R /srv/shiny-server/shinylearner/
ADD ui.R /srv/shiny-server/shinylearner/

EXPOSE 3838

CMD ["/usr/bin/shiny-server.sh"]
