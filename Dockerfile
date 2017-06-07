FROM srp33/shinylearner_environment:version6

COPY ShinyLearner.tar.gz /
RUN tar -zxf ShinyLearner.tar.gz

WORKDIR /
#ENTRYPOINT ["/scripts/docker_interface"]
