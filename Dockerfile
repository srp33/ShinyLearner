FROM srp33/shinylearner_environment:version63

COPY . /
RUN bash /scripts/build

WORKDIR /
