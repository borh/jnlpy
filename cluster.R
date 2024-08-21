cairo_pdf(file="cluster.pdf", onefile=TRUE, pointsize=11)#, family="Japan1", pointsize=8, onefile=TRUE)

basenames <- c(
#"モダリティ表現",
"言語表現形式"
#"モダリティ形式",
#"モダリティ副詞",
#"代名詞*",
##"副詞*",
#"助動詞*",
#"助詞係助詞",
#"助詞副助詞",
#"助詞接続助詞",
#"助詞格助詞",
##"助詞準体助詞",
#"助詞終助詞",
##"動詞一般",
##"動詞非自立可能",
##"名詞助動詞語幹", # doesnt work with PCA
##"名詞固有名詞",
##"名詞数詞",
##"名詞普通名詞",
##"形容詞一般",
##"形容詞非自立可能",
##"形状詞タリ",
##"形状詞一般",
##"形状詞助動詞語幹",
#"感動詞フィラー",
#"感動詞一般",
##"接尾辞動詞的",
##"接尾辞名詞的",
##"接尾辞形容詞的",
##"接尾辞形状詞的",
#"接続詞*"
#"接頭辞*",
##"空白*",
#"補助記号ＡＡ",
##"補助記号一般", # ?fail
#"補助記号句点",
#"補助記号括弧閉",
#"補助記号括弧開",
#"補助記号読点",
#"記号一般",
#"記号文字",
#"連体詞*"
)

library("pvclust")
library("FactoMineR")
library("Hmisc")

options(latexcmd='xelatex')
options(xdvicmd='xelatex')

top.sort <- function(p) {
  cnum <- ncol(p)
  cnames <- colnames(p)
  i <- 1
  while(i <= cnum) {
    latex(sort(p[,i], decreasing=TRUE)[1:8], title=cnames[i], dec=2, file=paste(name, "supl-data.tex", sep="-"), append=TRUE, longtable=TRUE)
    i <- i + 1
  }
}

generate.latex <- function(p, name, append=FALSE) {
  l.eig <- latex(p$eig[1:5,], dec=2, file=paste(name, "supl-data.tex", sep="-"), append=append, longtable=TRUE)
  top.sort(p$var$contrib)
  l.var <- latex(p$var$contrib, dec=2, file=paste(name, "supl-data.tex", sep="-"), append=TRUE, longtable=TRUE)
  top.sort(p$ind$contrib)
  l.ind <- latex(p$ind$contrib, dec=2, file=paste(name, "supl-data.tex", sep="-"), append=TRUE, longtable=TRUE)
  l.cal <- latex(t(p$call$X), dec=2, file=paste(name, "supl-data.tex", sep="-"), append=TRUE, longtable=TRUE)
}

batch.cluster <- function(posdata) {
  dist.methods <- c(
                    "euclidean",
                    "maximum"
                    #"manhattan",
                    #"canberra",
                    #"binary",
                    #"minkowski"
                    )
  dist.func <- function(x) {
    return (dist(posdata, method=x))
  }
  dist.all <- lapply(dist.methods, dist.func)

  cluster.methods <- c(
                       "ward",
                       "single"
                       #"complete",
                       #"average",
                       #"mcquitty",
                       #"median",
                       #"centroid"
                       )

  i <- 1
  for (d in dist.all) {
    for (m in cluster.methods) {
      fit <- hclust(d, method=m)
      plot(fit, main=paste(name, paste(dist.methods[i], m, sep=" x "))) # display dendogram
      groups <- cutree(fit, k=5) # cut tree into 5 clusters
      # draw dendogram with red borders around the 5 clusters
      rect.hclust(fit, k=5, border="red")
    }
    i <- i + 1
  }
  
}

for (name in basenames) {
  posdata <- read.table(paste(name, "clusterdata.tsv", sep="-"), header=TRUE, sep="\t", quote="")
  #posdata <- data.frame(posdata[-1], row.names=posdata[[1]], col.names=posdata[,1])
  tposdata <- t(posdata)
  #tposdata <- scale(tposdata)
  #posdata <- scale(posdata)

  print(name)
  p <- PCA(posdata, graph=FALSE)
  plot.PCA(p, c(1, 2), new.plot=FALSE, title=paste(name, "による主成分分析", sep=""))
  plot.PCA(p, c(2, 3), new.plot=FALSE, title=paste(name, "による主成分分析", sep=""))
  plot.PCA(p, c(2, 4), new.plot=FALSE, title=paste(name, "による主成分分析", sep=""))
  plot.PCA(p, c(2, 5), new.plot=FALSE, title=paste(name, "による主成分分析", sep=""))
  #print(name)
  #generate.latex(p, name)

  tp <- PCA(tposdata, graph=FALSE)
  plot.PCA(tp, c(1, 2), new.plot=FALSE, title=paste(name, "による主成分分析", sep=""))
  plot.PCA(tp, c(2, 3), new.plot=FALSE, title=paste(name, "による主成分分析", sep=""))
  plot.PCA(tp, c(2, 4), new.plot=FALSE, title=paste(name, "による主成分分析", sep=""))
  plot.PCA(tp, c(2, 5), new.plot=FALSE, title=paste(name, "による主成分分析", sep=""))
  #generate.latex(tp, name, append=TRUE)

  
  batch.cluster(posdata)
  batch.cluster(tposdata)
  #d.euclid <- dist(posdata, method = "euclidean") # distance matrix
  ##fit <- hclust(d, method="centroid")
  #fit <- hclust(d, method="ward")
  #fiti. <- hclust(d., method="ward")
  #plot(fit, main=name) # display dendogram
  #groups <- cutree(fit, k=5) # cut tree into 5 clusters
  ## draw dendogram with red borders around the 5 clusters
  #rect.hclust(fit, k=5, border="red")
}

#basenames <- c(
#"助詞係助詞",
#"助詞副助詞",
#"助詞接続助詞",
#"助詞格助詞",
#"助詞準体助詞",
#"助詞終助詞",
#"接続詞*"
#)
#
#library(snow)
#cl <- makeCluster(6, type="MPI")
#
#for (name in basenames) {
#  posdata <- read.table(paste(name, "clusterdata.tsv", sep="-"), header=TRUE)
#  posdata <- data.frame(posdata[-1], row.names=posdata[[1]])
#  posdata <- scale(posdata)
#
#  # Ward Hierarchical Clustering with Bootstrapped p values
#  fit <- parPvclust(cl, posdata, method.hclust="ward",
#                    method.dist="euclidean", nboot=100)
#  plot(fit) # dendogram with p values
#  # add rectangles around groups highly supported by the data
#  pvrect(fit, alpha=.95) 
#}
dev.off()
