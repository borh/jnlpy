cairo_pdf(file="natsume-comparison.pdf", onefile=TRUE, pointsize=8, width = 8, height = 5)#, family="Japan1", pointsize=8, onefile=TRUE)
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

library("pvclust")
#source("pvclust_unofficial_090824/pvclust.R")
#source("pvclust_unofficial_090824/pvclust-internal.R")

#library(MASS)

# Define a distance function. It should return an object of class "dist".
# Data should be "x" in the function and there should be "..." in the last of the argument list.

cosine <- function(x, ...) {
    x <- as.matrix(x)
    y <- t(x) %*% x
    res <- 1 - y / (sqrt(diag(y)) %*% t(sqrt(diag(y))))
    res <- as.dist(res)
    attr(res, "method") <- "cosine"
    return(res)
}

#library("FactoMineR")
#library("Hmisc")
#library("ggplot2")
#library("nFactors")
#library("psych")

#library("zipfR")

batch.cluster <- function(posdata, name) {
  tposdata <- as.data.frame(t(posdata))
  dist.methods <- c(
                    #cosine#,
                    "correlation"#,
                    ##"uncentered",
                    ##"abscor",
                    #"euclidean"
                    #"maximum",
                    ##"manhattan",
                    #"canberra",
                    ##"binary",
                    #"minkowski"
                    )
  cluster.methods <- c(
                       "ward"#,
                       #"single",
                       #"complete",
                       #"average"
                       #"mcquitty",
                       #"median",
                       #"centroid"
                       )
  for (d in dist.methods) {
    for (m in cluster.methods) {
      # suzuki clustering
      print(paste(str(d), m))
      #fit <- pvclust(tposdata, method.hclust=m, method.dist=d, nboot=1000)
      fit <- parPvclust(cl, tposdata, method.hclust=m, method.dist=d, nboot=1000)
      plot(fit, main=name) # dendogram with p values
      # add rectangles around groups highly supported by the data
      pvrect(fit, alpha=.95)
      print(fit)
      seplot(fit)
    }
  }
}

#par(mfrow=c(2,2))
#par(mar=c(3,3,2,1))

library("snow")
cl <- makeCluster(6, type="MPI")

collocations10k <- read.table("natsume-10000-summary.tsv", header=TRUE, sep="\t", quote="")
print(summary(collocations10k))
batch.cluster(collocations10k, "Natsumeの各コーパスにおける上位頻度10,000の共起")

collocations1k <- read.table("natsume-1000-summary.tsv", header=TRUE, sep="\t", quote="")
print(summary(collocations1k))
batch.cluster(collocations1k, "Natsumeの各コーパスにおける上位頻度1,000の共起")

collocations500 <- read.table("natsume-500-summary.tsv", header=TRUE, sep="\t", quote="")
print(summary(collocations500))
batch.cluster(collocations500, "Natsumeの各コーパスにおける上位頻度500の共起")


#for (name in basenames) {
#  #collocations <- read.table(paste("natsume-", name, "-10000.tsv", sep=""), col.names=c("n", "p", "v", "f"), header=FALSE, sep="\t", quote="")
#  collocations <- read.table(paste("natsume-", name, "-10000.tsv", sep=""), col.names=c("npv", "f"), header=FALSE, sep="\t", quote="")
#  print(name)
#  print(str(collocations))
## normalize
#  print(summary(collocations))
#}
dev.off()
