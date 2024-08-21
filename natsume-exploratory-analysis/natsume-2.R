#!/usr/bin/R -f
cairo_pdf(file="natsume-phd-poster.pdf", onefile=TRUE, pointsize=8, width = 8, height = 5)#, family="Japan1", pointsize=8, onefile=TRUE)
#png(filename = "2010-writing-systems-report.png",

basenames <- c(
"科学技術論文",
"自然言語処理",
"白書",
"Wikipedia",
"Yahoo!ブログ",
"Yahoo!知恵袋",
"国会会議録",
"新聞",
"検定教科書",
"流通書籍",
"生産書籍",
"ベストセラー",
"雑誌"
)

#library("pvclust")
#source("pvclust_unofficial_090824/pvclust.R")
#source("pvclust_unofficial_090824/pvclust-internal.R")

#library(MASS)

# Define a distance function. It should return an object of class "dist".
# Data should be "x" in the function and there should be "..." in the last of the argument list.

#library("FactoMineR")
#library("Hmisc")
#library("ggplot2")
#library("nFactors")
#library("psych")

#library("zipfR")

#par(mfrow=c(2,2))
#par(mar=c(3,3,2,1))

library(ggplot2)
library(MASS)
collocations10k <- read.table("natsume-500-summary.tsv", header=TRUE, sep="\t", quote="")
collocations10k.d <- dist(collocations10k) # euclidean distances between the rows
collocations10k.fit <- isoMDS(collocations10k.d, k=2) # k is the number of dim
collocations10k.pts <- data.frame(x=collocations10k.fit$points[,1], y=collocations10k.fit$points[,2])
print(collocations10k.pts)
ggplot(data=collocations10k.pts, aes(x, y)) + geom_point()
#colnames(collocations10k.pts) <- paste("M", 1:ncol(collocations10k.pts), sep="")
#collocations10k.ord <- cbind(data, collocations10k.pts)
#print(collocations10k.ord)
#ggplot(data=collocations10k.ord) + geom_points()

#batch.cluster(collocations10k, "Natsumeの各コーパスにおける上位頻度10,000の共起")

#collocations1k <- read.table("natsume-1000-summary.tsv", header=TRUE, sep="\t", quote="")
#print(summary(collocations1k))
##batch.cluster(collocations1k, "Natsumeの各コーパスにおける上位頻度1,000の共起")
#
#collocations500 <- read.table("natsume-500-summary.tsv", header=TRUE, sep="\t", quote="")
#print(summary(collocations500))
##batch.cluster(collocations500, "Natsumeの各コーパスにおける上位頻度500の共起")


#for (name in basenames) {
#  #collocations <- read.table(paste("natsume-", name, "-10000.tsv", sep=""), col.names=c("n", "p", "v", "f"), header=FALSE, sep="\t", quote="")
#  collocations <- read.table(paste("natsume-", name, "-10000.tsv", sep=""), col.names=c("npv", "f"), header=FALSE, sep="\t", quote="")
#  print(name)
#  print(str(collocations))
## normalize
#  print(summary(collocations))
#}
dev.off()
