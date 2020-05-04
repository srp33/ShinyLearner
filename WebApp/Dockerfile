FROM rocker/shiny-verse:3.6.1

RUN rm -rf /srv/shiny-server/* \
 && mkdir /srv/shiny-server/ShinyLearner

COPY . /srv/shiny-server/ShinyLearner/

WORKDIR /srv/shiny-server

USER shiny
