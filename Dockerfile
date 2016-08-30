FROM srp33/shinylearner_environment:version1

COPY ShinyLearner.tar.gz ~/

RUN tar -zxvf ShinyLearner.tar.gz
#VOLUME /ShinyLearner/v
#WORKDIR /ShinyLearner
#ENTRYPOINT ["./docker_nc_mc.sh"]
