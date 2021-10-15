#for (package in c("mlr"))
for (package in c("extraTrees"))
  install.packages(package, repos="http://cran.us.r-project.org", dependencies=TRUE)
