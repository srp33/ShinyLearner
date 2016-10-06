FROM srp33/shinylearner_environment:version2

COPY ShinyLearner.tar.gz /
RUN tar -zxf ShinyLearner.tar.gz

WORKDIR /
ENTRYPOINT ["/scripts/docker_interface"]
