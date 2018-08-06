FROM srp33/shinylearner_environment:version40

COPY ShinyLearner.tar.gz /
RUN tar -zxf ShinyLearner.tar.gz; rm ShinyLearner.tar.gz

WORKDIR /
