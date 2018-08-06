FROM srp33/shinylearner_environment:version35

RUN scripts/build

COPY shinylearner.jar /
COPY scripts /
COPY AlgorithmScripts /
COPY README.md /
COPY VERSION /
COPY LICENSE /
COPY UserScripts /

#COPY ShinyLearner.tar.gz /
#RUN tar -zxf ShinyLearner.tar.gz; rm ShinyLearner.tar.gz

WORKDIR /
