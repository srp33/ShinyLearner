suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(readr))
suppressPackageStartupMessages(library(magrittr))

inFilePath <- commandArgs()[7]
sortColumns <- strsplit(commandArgs()[8], ",")[[1]]
outFilePath <- commandArgs()[9]

# See https://gist.github.com/skranz/9681509
eval.string.dplyr = function(.data, .fun.name, ...) {
  args = list(...)
  args = unlist(args)
  code = paste0(.fun.name,"(.data,", paste0(args, collapse=","), ")")
  df = eval(parse(text=code,srcfile=NULL))
  df  
}

# See https://gist.github.com/skranz/9681509
s_arrange = function(.data, ...) {
  eval.string.dplyr(.data,"arrange", ...)
}

read_tsv(inFilePath) %>% s_arrange(commandArgs()[8]) %>% write_tsv(outFilePath)
