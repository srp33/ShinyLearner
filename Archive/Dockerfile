#Eventually, we need to combine the RUN commands into a single RUN command, but for now it is helpful to have them separate (that way we do not have to recompile the R packages every time we rebuild)
#The downside to separate RUN commands is that Docker saves intermediate images (in this case, each is about 1 Gig). So after multiple builds it adds up. They can be erased with the following command
#docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
FROM java:8u91-jre
#Install R + Packages
RUN echo "deb http://cran.cnr.berkeley.edu/bin/linux/debian jessie-cran3/" >> /etc/apt/sources.list \
  && apt-get update \
  && apt-get -y --force-yes install libcurl4-openssl-dev r-base-core \
  && R -e "install.packages('dplyr',repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('knitr',repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('rmarkdown',repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('readr',repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('AUC',repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('RankAggreg', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('ggplot2', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('mlr', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('randomForestSRC', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('mRMRe', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('nnet', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('kohonen', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('adabag', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('rpart', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('C50', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('party', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('glmnet', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('deepnet', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('extraTrees', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('FNN', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('kernlab', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('gbm', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('DescriMiner', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('h2o', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('kknn', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('class', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('MASS', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('LiblineaR', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('mda', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('RSNNS', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('e1071', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('randomForest', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('ranger', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('klaR', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('rFerns', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('rknn', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('RRF', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('rrlda', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('sda', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('sparseLDA', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('elasticnet', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('xgboost', repos='https://rweb.crmda.ku.edu/cran/')" \
  && R -e "install.packages('ROCR',repos='https://rweb.crmda.ku.edu/cran/')"
##Install Scikit-Learn (non-MKL)
RUN wget --quiet https://repo.continuum.io/miniconda/Miniconda2-4.0.5-Linux-x86_64.sh -O ~/miniconda.sh \
  && /bin/bash ~/miniconda.sh -b -p /opt/conda \ 
  && rm ~/miniconda.sh \
  && /opt/conda/bin/conda install -y nomkl scikit-learn pandas conda-build \
  && /opt/conda/bin/conda clean --all
##Add python to PATH
ENV PATH /opt/conda/bin:$PATH
###Install Pandoc
RUN apt-get -y install pandoc
#Cleanup R 
RUN find /usr/local/lib/R/site-library/ -depth -wholename '*/html' -exec rm -r "{}" \; \
  && find /usr/local/lib/R/site-library/ -depth -wholename '*/data' -exec rm -r "{}" \; \
  && find /usr/local/lib/R/site-library/ -depth -wholename '*/doc' -exec rm -r "{}" \; \
  && find /usr/local/lib/R/site-library/ -depth -wholename '*/tests' -exec rm -r "{}" \; \
  && find /usr/local/lib/R/site-library/ -depth -wholename '*/examples' -exec rm -r "{}" \; \
  && find /usr/local/lib/R/site-library/ -depth -wholename '*/help' -exec rm -r "{}" \; \
  && find /usr/local/lib/R/site-library/ -depth -wholename '*/www' -exec rm -r "{}" \; \
  && find /usr/local/lib/R/site-library/ -depth -wholename '*/www-dir' -exec rm -r "{}" \; \
  && find /usr/local/lib/R/site-library/ -depth -wholename '*/staticdocs' -exec rm -r "{}" \; \
  && find /usr/local/lib/R/site-library/ -depth -wholename '*/demo' -exec rm -r "{}" \; \
  && find /usr/lib/R/library/ -depth -wholename '*/html' -exec rm -r "{}" \; \
  && find /usr/lib/R/library/ -depth -wholename '*/data' -exec rm -r "{}" \; \
  && find /usr/lib/R/library/ -depth -wholename '*/doc' -exec rm -r "{}" \; \
  && find /usr/lib/R/library/ -depth -wholename '*/tests' -exec rm -r "{}" \; \
  && find /usr/lib/R/library/ -depth -wholename '*/examples' -exec rm -r "{}" \; \
  && find /usr/lib/R/library/ -depth -wholename '*/help' -exec rm -r "{}" \; \
  && find /usr/lib/R/library/ -depth -wholename '*/www' -exec rm -r "{}" \; \
  && find /usr/lib/R/library/ -depth -wholename '*/www-dir' -exec rm -r "{}" \; \
  && find /usr/lib/R/library/ -depth -wholename '*/staticdocs' -exec rm -r "{}" \; \
  && find /usr/lib/R/library/ -depth -wholename '*/demo' -exec rm -r "{}" \; \
  && rm -rf /usr/local/lib/R/site-library/BH
RUN apt-get -y install git
##Cleanup Debian
RUN apt-get -y remove cpp-4.9 && apt-get -y autoremove \
  && rm -rf /usr/share/mime /usr/share/mime /usr/share/perl /usr/share/tcltk /usr/share/man \
  && rm -rf /usr/share/doc /usr/share/locale /usr/share/perl5
##Install ML-Flex-Lite
#COPY . /ShinyLearner/
RUN git clone https://github.com/srp33/ShinyLearner.git
VOLUME /ShinyLearner/v
WORKDIR /ShinyLearner
ENTRYPOINT ["./docker_nc_mc.sh"]
