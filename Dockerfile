FROM srp33/shinylearner_environment:version1

COPY ShinyLearner.tar.gz /
RUN tar -zxvf ShinyLearner.tar.gz

WORKDIR /
ENTRYPOINT ["/scripts/docker_interface"]
