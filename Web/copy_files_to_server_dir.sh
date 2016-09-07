#!/bin/bash

# Server Conf
cp -r /home/tjlee3/shiny-server.conf /etc/shiny-server/shiny-server.conf

# ShinyLearner
mkdir -p /srv/shiny-server/shinylearner
cp -r /home/tjlee3/shinylearner/* /srv/shiny-server/shinylearner/
