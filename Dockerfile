FROM srp33/shinylearner_environment:version1

COPY ShinyLearner.tar.gz /

RUN cd / \
  && tar -zxvf ShinyLearner.tar.gz \
  && TestScripts/nestedclassification_montecarlo

t#VOLUME /ShinyLearner/v
#WORKDIR /ShinyLearner
#ENTRYPOINT ["./docker_nc_mc.sh"]
