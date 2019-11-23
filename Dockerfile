FROM srp33/shinylearner_environment:version60

COPY . /
RUN bash /scripts/build

WORKDIR /
