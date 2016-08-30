FROM srp33/shinylearner_environment:version1

COPY ShinyLearner.tar.gz /

RUN tar -zxvf ShinyLearner.tar.gz

VOLUME /data
WORKDIR /
ENTRYPOINT ["/scripts/docker_interface"]
