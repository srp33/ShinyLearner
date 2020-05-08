FROM rocker/shiny-verse:3.6.1

RUN rm -rf /srv/shiny-server/* \
 && mkdir /srv/shiny-server/shinylearner

COPY . /srv/shiny-server/shinylearner/

WORKDIR /srv/shiny-server

USER shiny
