FROM rocker/shiny-verse:3.6.1

RUN rm -rf /srv/shiny-server/*

COPY . /srv/shiny-server/

WORKDIR /srv/shiny-server

USER shiny
