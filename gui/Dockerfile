FROM rocker/shiny:latest

#ADD server.R /srv/shiny-server/shinylearnerweb/
#ADD ui.R /srv/shiny-server/shinylearnerweb/
#ADD www /srv/shiny-server/shinylearnerweb/
#ADD ShinyLearner /srv/shiny-server/shinylearnerweb/

## Install packages from CRAN
RUN R -e "install.packages(c('shiny'))"

COPY ./shinylearnerweb/ /srv/shiny-server/shinylearnerweb/

#EXPOSE 3838

#CMD ["/usr/bin/shiny-server.sh"]
