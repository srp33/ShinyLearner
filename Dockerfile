FROM srp33/shinylearner_environment:version69

COPY . /
RUN bash /scripts/build

WORKDIR /
