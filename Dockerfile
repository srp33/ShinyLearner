FROM srp33/shinylearner_environment:version1

COPY release/shinylearner.jar ~/
COPY scripts/* ~/scripts/

#RUN git clone https://github.com/srp33/ShinyLearner.git
#VOLUME /ShinyLearner/v
#WORKDIR /ShinyLearner
#ENTRYPOINT ["./docker_nc_mc.sh"]
