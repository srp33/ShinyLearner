FROM srp33/shinylearner_environment:version8

COPY ShinyLearner.tar.gz /
RUN tar -zxf ShinyLearner.tar.gz; rm ShinyLearner.tar.gz

WORKDIR /
#ENTRYPOINT ["/scripts/docker_interface"]
