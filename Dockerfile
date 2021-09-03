FROM srp33/shinylearner_environment:version61

COPY . /
RUN bash /scripts/build

WORKDIR /
