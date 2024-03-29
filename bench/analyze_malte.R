#! /usr/bin/env Rscript

# in inches
figure.width <- 7
ratio <- 2/3
figure.height <- 2.3
# figure.height <- 1.4

blacklist <- c()
group.by <- c("vm","benchmark")
reference <- ''

input.basename <- 'CopSurvey'

tsv_names.default <- list.files(pattern="malte-.*.tsv")

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
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
  setwd("~/Documents/Uni/Paper/cop2016-sidewayscomp/bench")
  cmd.line <- FALSE
  tsv_names <- tsv_names.default
} else {
  cmd.line <- TRUE
  tsv_names <- tsv_names.cmd.line(tsv_names.default)
}
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


bench <- (function () {
  df <- data.frame()
  for (vm in tsv_names) {
    desc <- unlist(strsplit(first(unlist(strsplit(tsv, '.', fixed=TRUE))), '-'))
    category <- desc[[1]]
    #   implementation <- desc[[2]]
    os <- desc[[3]]
    vm <- desc[[4]]
    print(paste('reading', tsv));
    vm_bench <- read.delim(tsv, sep="\t", comment.char = "#", header=TRUE, stringsAsFactors=FALSE,strip.white=TRUE,
                          col.names=c('name', 'ops', 'time', 'value'))
    vm_bench <- vm_bench[!grepl('^Wrapper', vm_bench$name),,drop=TRUE]
    vm_bench$name <- sapply(vm_bench$name, function(x) {sedit(x, 'Method:', 'Method')})
    vm_bench$name <- sapply(vm_bench$name, function(x) {sedit(x, '_', ':')})
    vm_bench$os <- os
    
    #   vm_bench$category <- category                    
    sub_bench <- read.table(sep=":",text=as.character(vm_bench$name), col.names=c('impl', 'benchmark', 'variable_values'))
    vm_bench$vm <- paste(sub_bench$impl, capitalize(vm))
    vm_bench <- cbind(vm_bench, sub_bench[c('benchmark','variable_values')])  
    df <- rbind(df, vm_bench)}
  df
})()

bench <- bench[c('os','vm','benchmark','variable_values','ops', 'time', 'value')]

# bench <- droplevels(bench[bench$criterion != 'gc',,])
bench$benchmark <- factor(bench$benchmark, levels = c('ActivateLayer','ActivateLayerFlat','MethodStandard', 'MethodNoLayer','MethodWithLayer')) 

# --- shaping data

# num.vms <- length(levels(factor(bench$vm)))
num.vms <- length(levels(factor(paste(bench$os, bench$vm))))
num.runs <- length(bench$benchmark)
num.benches <- length(levels(bench$benchmark))
num.vars <- length(levels(factor(bench$variable_values)))
# num.crit <- length(levels(bench$criterion))
num.crit <- 1

if (num.vars == 0) {
  num.vars <- 1
}
rigorous <- num.runs > (num.vms * num.benches * num.vars * num.crit)

# bench <- fill.missing(bench)


######################################################

stop('Bis hier her.')

bench.summary <- summarize.bench(bench, rigorous, FALSE, group.by, reference)


bench.summary.graph <- data.frame(bench.summary)

# bench.summary.graph <- droplevels(bench.summary[bench.summary$benchmark %ni% generic,,drop=TRUE])
# bench.summary.generic <- droplevels(bench.summary[bench.summary$benchmark %in% generic,,drop=TRUE])
# bench.summary.generic$benchmark <- gsub("-generic","\ngeneric",bench.summary.generic$benchmark)


# order by mean

# bench.summary.graph$benchmark <- reorder(bench.summary.graph$benchmark, bench.summary.graph$mean.norm,
#                                          function(x) {if (x[[1]] > 1.0) { max(x) } else { min(x) }})

bench.summary.graph$vm <- reorder(bench.summary.graph$vm, bench.summary.graph$mean.norm,
                                         function(x) {if (x[[1]] > 1.0) { max(x) } else { min(x) }})


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
rownames(bench.summary.ltx) <- bench.summary.sel$vm
colnames(bench.summary.ltx) <- sapply(colnames(bench.summary.ltx), function(x) {sedit(x, '_', ' ')})

# ----- Outputting -----

# Excel for overall data
write.xlsx(bench, paste0(input.basename, ".xlsx"), append=FALSE, sheetName="bench")
write.xlsx(bench.summary, paste0(input.basename, ".xlsx"), append=TRUE, sheetName="summary")

dodge <- position_dodge(width=.75)
ymax <- round_any(max(bench.summary.graph$mean.norm, na.rm=TRUE), 0.5, ceiling)

# -------------------------------- Normal -----------------------------------------
p <- ggplot(data=bench.summary.graph,
#        aes(x=benchmark,y=mean.norm,group=interaction(benchmark,vm),fill=vm,)
       aes(x=vm,y=mean.norm,group=interaction(vm,benchmark),fill=benchmark,)
) + default.theme() +
#   geom_bar(stat="identity", position=dodge, width=.6, aes(fill = vm))+
  geom_bar(stat="identity", position=dodge, width=.6, aes(fill = benchmark))+
#   geom_point(position=dodge,aes(y=0.15, ymax=ymax, shape=vm),size=2, color="grey90",stat="identity") +
  geom_point(position=dodge,aes(y=0.15, ymax=ymax, shape=benchmark),size=2, color="grey90",stat="identity") +
  ylab("Relative Runtime") +
  scale_y_continuous(breaks=seq(0,ymax,1), limits=c(0,ymax),expand=c(0,0)) +
  scale_fill_brewer(name = "Virtual Machine", type="qual", palette="Set1", guide="none") 
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
    len <- ncol(bench.summary.ltx)/2
    .just = rep(c('r','@{}>{\\smaller\\ensuremath{\\pm}}r@{\\,\\si{\\milli\\second}}'), len)
    .just = c('@{}r', .just[2:length(.just)])
    out <- latex(bench.summary.ltx,
                 file=paste0(input.basename, "-all.tex"),
                 rowlabel="Benchmark",
                 caption="All Shootout benchmarks results",
                 lines.page=999999,
                 booktabs=TRUE,
                 center="none",
                 longtable=TRUE,
                 size="small", #center="centering",
                 colheads=rep(c('mean', ''), len),
                 col.just=.just,
                 #col.just=rep(c('r','@{\\,\\si{\\milli\\second} \\ensuremath{\\pm}}r'), len),
                 cgroup=levels(as.factor(bench.summary$vm)),
                 cdec=rep(0, len*2))
  })()
  
} else {
  # LaTeX table, all
  (function() {
    if (nrow(bench.summary.ltx) <= 0) return()
    colnames(bench.summary.ltx) <- gsub(' mean', '', colnames(bench.summary.ltx))  
    len <- ncol(bench.summary.ltx)
    .just = rep('@{}r', len)
    .long <- nrow(bench.summary.ltx) > 50
    out <- latex(bench.summary.ltx,
                 file=paste0(input.basename, "-all.tex"),
                 rowlabel="Benchmark",
                 booktabs=TRUE,
                 lines.page=999999,
                 table.env=(! .long), center="none",
                 longtable=.long,
                 size="small", #center="centering",
                 col.just=.just,
                 cdec=rep(0, len))
  })()
}

bench.info <- bench.summary.graph[bench.summary.graph$overall == FALSE,,] 

winners <- bench.info %>% group_by(benchmark) %>% filter(mean.norm == min(mean.norm))
winners <- winners[c('mean.norm','benchmark','vm')]
winners <- winners[do.call(order, winners),]

print(">> done");
