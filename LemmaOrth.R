####d <- read.csv("terry2010-lemma-orth-relations.csv", header=TRUE)
####
####source("normalize.R")
####
####wstd <- data.frame(d[,7:12], row.names=d[,1])
####
####nrwstd <- wstd
####for (i in 1:length(wstd[1,])) {
####  nrwstd[,i] <- normalize(wstd[,i])
####}
####
####ncwstd <- wstd
####for (i in 1:length(wstd[,1])) {
####  ncwstd[i,] <- normalize(wstd[i,])
####}
####
####
#####library("RColorBrewer")
####library("colorspace")
#####mycolors <- c(brewer.pal(9, "Set1"), brewer.pal(8, "Set2"), brewer.pal(12, "Set3"),  brewer.pal(12, "Paired"), brewer.pal(8, "Dark2"))[1:37]
####mycolors <- rainbow_hcl(37, start=0, end=360)
####
####library("plotrix")
####barp(nrwstd, names.arg=colnames(nrwstd), legend.lab=rownames(nrwstd), col=mycolors)

# test for fukusi
f <- read.csv("lemma-orth-relations-副詞-*.tsv", header=TRUE, sep="\t")

flemma <- f$lemma

#fh <- table()

lf <- length(f$lemma)

for (n in seq(from=10, to=5)) {
  print (n)
  for (i in 1:lf) {
    print (i)
    currlemma <- flemma[i]
    accu <- c()
    if ((length(flemma[flemma==currlemma]) > n) & (length(accu[accu==currlemma]) < 1)) {
      accu <- c(accu, flemma[i])
      #print (n)
      #print (f$lemma[i])
    }
    print (accu)
  }
}
