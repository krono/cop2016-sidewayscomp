#! /usr/bin/env Rscript

# in inches
figure.width <- 7
# ratio <- 2/3
ratio <- 3/4
figure.height <- 2.3
# figure.height <- 1.4


do.only.nothing <- TRUE
all.mean.in.graph <- TRUE
all.mean.in.graph.shootout <- FALSE
MAX.CROSS <- 3

blacklist <- c()
# reference.vm <- 'Python'
#reference.benchmark <- 'Red'



input.basename <- 'DeltaBlue'
bench_names <- c('deltablue') #, 'richards')
tsv_names.default <- c('python', 'pypy', 'pypypromote')


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
if (FALSE) {
  setwd("~/Documents/Uni/Paper/cop2016-sidewayscomp/bench")
  cmd.line <- FALSE
} else {
  cmd.line <- TRUE
}   

pkgs = c(
  "reshape2",
  "plyr",
  #"beanplot",
  "boot",
  "Hmisc",
  "ggplot2",
  "tools",
  "xlsx",
  "dplyr"
)
source("./help.R")

if (FALSE) {
  tsv_names <- tsv_names.default
} else {
  tsv_names <- tsv_names.cmd.line(tsv_names.default, check=FALSE)
}
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


.bench <- data.frame()
.bench.summary <- data.frame()

for (bench_name in bench_names) {
  if (bench_name == 'deltablue') {
    bench_levels = c('DeltaBlue', 'DeltaPurple', 'DeltaViolet','DeltaRed')
    reference.benchmark <- 'DeltaBlue'
  } else if (bench_name == 'richards') {
    bench_levels = c('Richards','RichardsViolet','RichardsRed')
    reference.benchmark <- 'Richards'
  } else {stop ("why?")}
  
bench <- (function () {
  .vm.name <- function(src) {
    if (src == 'pypy')
      'PyPy'
    else if (src == 'python')
      'Python'
    else if (src == 'pypypromote')
      'ContextPyPy'
    else
      src
  }
  df <- data.frame(vm=factor(levels= c('Python', 'PyPy', 'ContextPyPy')))
  for (vm in tsv_names) {
    tsv_name <- last(vm)
    vm_bench <- read.delim(paste0(bench_name, '-contextpy-osx-',tsv_name,'.tsv'), comment.char = "#", header=TRUE,
                          col.names=c('benchmark', 'value'))
    vm_bench$bench <- capitalize(bench_name)
    vm_bench$vm <- factor(.vm.name(vm))
    df <- rbind(df, vm_bench)}
  df
})()

bench$vm <- factor(bench$vm, levels= c('Python', 'PyPy', 'ContextPyPy'))
bench$benchmark <- factor(bench$benchmark, levels=bench_levels) 

# --- shaping data

bench <- droplevels(bench[!(bench$benchmark %in% blacklist),,])
# bench <- bench[c('criterion','vm','benchmark','value', 'variable_values')]
# bench <- bench[c('vm','benchmark','value')]
# bench <- bench[c('bench','vm','benchmark','value')]

num.vms <- length(levels(factor(bench$vm)))
num.runs <- length(bench$benchmark)
num.benches <- length(levels(bench$benchmark))
# num.vars <- length(levels(factor(bench$variable_values)))
# num.crit <- length(levels(bench$criterion))
num.vars <- 1
num.crit <- length(levels(factor(bench$bench)))

if (num.vars == 0) {
  num.vars <- 1
}
rigorous <- num.runs > (num.vms * num.benches * num.vars * num.crit)

bench <- fill.missing(bench)


######################################################


group.by <- c("vm","benchmark")

.bench.summary <- rbind(.bench.summary, summarize.bench(bench, rigorous, FALSE, group.by, reference.benchmark))
.bench <- rbind(.bench, bench)
}

bench <- .bench
bench.summary <- .bench.summary

bench.summary.graph <- data.frame(bench.summary)

# bench.summary.graph <- droplevels(bench.summary[bench.summary$benchmark %ni% generic,,drop=TRUE])
# bench.summary.generic <- droplevels(bench.summary[bench.summary$benchmark %in% generic,,drop=TRUE])
# bench.summary.generic$benchmark <- gsub("-generic","\ngeneric",bench.summary.generic$benchmark)


# order by mean

# bench.summary.graph$benchmark <- reorder(bench.summary.graph$benchmark, bench.summary.graph$mean.norm,
#                                          function(x) {if (x[[1]] > 1.0) { max(x) } else { min(x) }})

# bench.summary.graph$vm <- reorder(bench.summary.graph$vm, bench.summary.graph$mean.norm,
#                                   function(x) {if (x[[1]] > 1.0) { max(x) } else { min(x) }})


# .selection <- c('vm','mean.norm')
# .ids <- c('vm')
# .group.by <- as.quoted(c("vm"))
# .selection <- c('benchmark','mean.norm')
# .ids <- c('benchmark')
# .group.by <- as.quoted(c("benchmark"))
# 
# bench.summary.overall <- ddply(melt(bench.summary.graph[.selection], id.vars=.ids), .group.by,
#                                plyr::summarize, 
#                                overall=TRUE,
# #                                benchmark='geometric\nmean',
#                                vm='geometric\nmean',
#                                mean=1,
#                                mean.norm=geomean(value),
#                                median=1
# )
# print(">>>> OVERALL\n")
# print(bench.summary.overall)
# 
# if (rigorous) {
#   bench.summary.overall <- merge(bench.summary.overall, data.frame(stdev=1, err095=1, cnfIntHigh=1,
#                                                                    cnfIntLow=1, conf=1, upper=NA, lower=NA))
# }
# bench.summary.graph <- rbind(bench.summary.graph, bench.summary.overall)  

sel.col = if (rigorous) { c(group.by[[1]], group.by[[2]],'mean','err095') }  else 
                        { c(group.by[[1]], group.by[[2]],'mean') }

bench.summary.sel <- dcast(melt(bench.summary[sel.col], id.vars=group.by), benchmark ~ vm + variable)
# bench.summary.sel <- dcast(melt(bench.summary[sel.col], id.vars=group.by), vm ~ benchmark + variable)
bench.summary.ltx <- bench.summary.sel[2:length(bench.summary.sel)]
# rownames(bench.summary.ltx) <- bench.summary.sel$benchmark
# # rownames(bench.summary.ltx) <- bench.summary.sel$vm
# colnames(bench.summary.ltx) <- sapply(colnames(bench.summary.ltx), function(x) {sedit(x, '_', ' ')})
# rownames(bench.summary.ltx) <- bench.summary.sel$vm
.fmt <- function(x) {
  format(round(x / 1e3), nsmall=0,justify=c("left"),width=0)
}
bench.summary.ltx <- data.frame(
  Python = paste(.fmt(bench.summary.sel$Python_mean), .fmt(bench.summary.sel$Python_err095), sep = ' +- '),
  PyPy = paste(.fmt(bench.summary.sel$PyPy_mean), .fmt(bench.summary.sel$PyPy_err095), sep = ' +- '),
  ContextPyPy = paste(.fmt(bench.summary.sel$ContextPyPy_mean), .fmt(bench.summary.sel$ContextPyPy_err095), sep = ' +- ')
)
rownames(bench.summary.ltx) <- bench.summary.sel$benchmark


# ----- Outputting -----

# Excel for overall data
write.xlsx(bench, paste0(input.basename, ".xlsx"), append=FALSE, sheetName="bench")
write.xlsx(bench.summary, paste0(input.basename, ".xlsx"), append=TRUE, sheetName="summary")

dodge <- position_dodge(width=.75)

if (FALSE){ # Me no want ya

ymax <- round_any(max(bench.summary.graph$cnfIntHigh/1e6, na.rm=TRUE), .5, ceiling)

# -------------------------------- Absolute -----------------------------------------
p <- ggplot(data=bench.summary.graph,
#        aes(x=benchmark,y=mean.norm,group=interaction(benchmark,vm),fill=vm,)
       aes(x=vm,y=mean/1e6,group=interaction(vm,benchmark),fill=benchmark,)
) + default.theme() +
  theme(
    axis.text.x  = element_text(size=6, angle=0, hjust=0.5),
    axis.text.y  = element_text(size=5),
    legend.position=c(0.75, .8),
    plot.margin = unit(c(.2,0,-2,-0.5),"mm")) +
#   geom_bar(stat="identity", position=dodge, width=.6, aes(fill = vm))+
  geom_bar(stat="identity", position=dodge, width=.6, aes(fill = benchmark))+
#   geom_point(position=dodge,aes(y=0.15, ymax=ymax, shape=vm),size=2, color="grey90",stat="identity") +
  geom_point(position=dodge,aes(y=1, ymax=ymax, shape=benchmark),size=2, color="grey90",stat="identity") +
  ylab("Absolute Runtime in seconds") +
  scale_y_continuous(breaks=seq(0,ymax,2), limits=c(0,ymax),expand=c(0,0)) +
  scale_fill_manual(name = "Benchmark", values = c("blue", "purple", "violet", "red")) +
#   scale_fill_brewer(name = "Benchmark", type="qual", palette="Set1") +
  scale_shape(name = "Benchmark", solid = FALSE) 
# +
#   facet_grid(. ~ overall, scales="free", space="free",labeller=label_bquote(""))
if (rigorous) {
  p <- p + geom_errorbar(aes(ymin=cnfIntLow/1e6, ymax=cnfIntHigh/1e6),  position=dodge, color=I("black"), size=.2)  
}

p

gg.file <- paste0(input.basename, ".pdf")
ggsave(gg.file, width=figure.width * ratio, height=figure.height * 1.35, units=c("in"), colormodel='rgb', useDingbats=FALSE)
embed_fonts(gg.file, options=pdf.embed.options)

}
# -------------------------------- Normal -----------------------------------------
ymax <- round_any(max(bench.summary.graph$mean.norm, na.rm=TRUE), 0.5, ceiling)
p <- ggplot(data=bench.summary.graph,
            #        aes(x=benchmark,y=mean.norm,group=interaction(benchmark,vm),fill=vm,)
            aes(x=vm,y=mean.norm,group=interaction(vm,benchmark),fill=benchmark,)
) + default.theme() +
  theme(
    axis.text.x  = element_text(size=6, angle=0, hjust=0.5),
    legend.position=c(0.75, .8),
    plot.margin = unit(c(0,0,-2,-0.5),"mm")) +
  #   geom_bar(stat="identity", position=dodge, width=.6, aes(fill = vm))+
  geom_bar(stat="identity", position=dodge, width=.6, aes(fill = benchmark))+
  #   geom_point(position=dodge,aes(y=0.15, ymax=ymax, shape=vm),size=2, color="grey90",stat="identity") +
  geom_point(position=dodge,aes(y=0.15, ymax=ymax, shape=benchmark),size=2, color="grey90",stat="identity") +
  ylab("Relative Runtime") +
  scale_y_continuous(breaks=seq(0,ymax,.5), limits=c(0,ymax),expand=c(0,0)) +
  scale_fill_manual(name = "Benchmark", values = c("blue", "purple", "violet", "red")) +
#     scale_fill_brewer(name = "Benchmark", type="qual", palette="Set1") +
  scale_shape(name = "Benchmark", solid = FALSE) 
# +
#   facet_grid(. ~ overall, scales="free", space="free",labeller=label_bquote(""))
if (rigorous) {
  p <- p + geom_errorbar(aes(ymin=lower, ymax = upper),  position=dodge, color=I("black"), size=.2)  
}

p

gg.file <- paste0(input.basename, "-norm.pdf")
ggsave(gg.file, width=figure.width * ratio, height=figure.height, units=c("in"), colormodel='rgb', useDingbats=FALSE)
embed_fonts(gg.file, options=pdf.embed.options)

if (rigorous) {
  # LaTeX table, all
  (function() {
    if (nrow(bench.summary.ltx) <= 0) return()
    file <- paste0(input.basename, "-all.tex")
#     cat("\\toprule\n", file=file)
#     cat("\\multicolumn{1}{c}{Benchmark} & \\multicolumn{1}{c}{", file=file, append=TRUE)
#     cat(paste0(colnames(bench.summary.ltx),collapse="} & \\multicolumn{1}{c}{"), file=file, append = TRUE)
#     cat("} \\\\\n",file=file, append = TRUE)
#     cat("\\midrule\n", file=file, append=TRUE)
#     write.table(bench.summary.ltx, file=file, append=TRUE, sep=" & ", quote=FALSE, eol=" \\\\\n", col.names=FALSE)
#     cat("\\bottomrule\n", file=file, append=TRUE)
    write.table(bench.summary.ltx, file=file, sep=" & ", quote=FALSE, eol=" \\\\\n", col.names=FALSE)
  })()
} else {
  stop('Stop and go back!.')
}

bench.info <- bench.summary.graph[bench.summary.graph$overall == FALSE,,] 

winners <- bench.info %>% group_by(benchmark) %>% filter(mean.norm == min(mean.norm))
winners <- winners[c('mean.norm','benchmark','vm')]
winners <- winners[do.call(order, winners),]

print(">> done");
