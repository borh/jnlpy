#cairo_pdf(file="report-factor.pdf", onefile=TRUE, pointsize=6)#, family="Japan1", pointsize=8, onefile=TRUE)
#cairo_pdf(file="final-adverbs-73-500000.pdf", onefile=TRUE, pointsize=6)#, family="Japan1", pointsize=8, onefile=TRUE)

basenames <- c(
#"モダリティ表現"
#"言語形式"
#"形状詞助動詞語幹",
#"形容詞非自立可能",
#"副詞*",
#"助詞終助詞",
#"接尾辞形容詞的",
#"助動詞*",
#"感動詞一般",
#"言語形式"
#               "Morphemes",
#               "Functional expressions",
#               "Suppositional adverbs"
#               "suppositional-adverbs-11",
               "Cluster dendrogram of corpora using suppositional adverbs"
#               "functional-expressions-11",
#               "Cluster dendrogram of corpora using functional expressions"
#"助詞接続助詞",
#"連体詞*",
#"接尾辞名詞的",
##"感動詞フィラー",
##"助詞準体助詞",
#"助詞副助詞",
#"接頭辞*",
#"助詞係助詞",
#"助詞格助詞",
#"接続詞*",
#"形状詞タリ",
##"形容詞一般",
##"形状詞一般",
#"代名詞*",
#"接尾辞形状詞的",
#"接尾辞動詞的"
#"JStage-言語形式"
#"流通書籍-言語形式",
#"JNLP-Journal-言語形式",
#"国会会議録-言語形式",
#"Yahoo!ブログ-言語形式",
#"Yahoo!知恵袋-言語形式",
#"インタービュー-言語形式"

##"ベストセラー-言語形式",
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

#library("pvclust")
source("pvclust_unofficial_090824/pvclust.R")
source("pvclust_unofficial_090824/pvclust-internal.R")

library(MASS)

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



library("FactoMineR")
library("Hmisc")
library("ggplot2")
library("nFactors")
library("psych")

options(latexcmd='xelatex')
options(xdvicmd='xelatex')

top.sort <- function(p, name) {
  cnum <- ncol(p)
  cnames <- colnames(p)
  i <- 1
  print (cnum)
  print (name)
  while(i <= cnum) {
    print (i)
    latex(sort(p[,i], decreasing=TRUE)[1:8], title=cnames[i], dec=2, file=paste(name, "supl-data.tex", sep="-"), append=TRUE, longtable=TRUE)
    i <- i + 1
  }
}

generate.latex <- function(p, name, append=FALSE) {
  l.eig <- latex(p$eig[1:5,], dec=2, file=paste(name, "supl-data.tex", sep="-"), append=append, longtable=TRUE)
  top.sort(p$var$contrib, name)
  l.var <- latex(p$var$contrib, dec=2, file=paste(name, "supl-data.tex", sep="-"), append=TRUE, longtable=TRUE)
  #print ("generating latex")
  #top.sort(p$ind$contrib, name)
  l.ind <- latex(p$ind$contrib, dec=2, file=paste(name, "supl-data.tex", sep="-"), append=TRUE, longtable=TRUE)
  l.cal <- latex(t(p$call$X), dec=2, file=paste(name, "supl-data.tex", sep="-"), append=TRUE, longtable=TRUE)
}

batch.cluster <- function(posdata, name) {
  tposdata <- as.data.frame(t(posdata))
  #library(snow)
  #cl <- makeCluster(6, type="MPI")

  #fit <- parPvclust(cl, tposdata, method.hclust="ward",
  #                  method.dist="euclidean", nboot=1000)
  #plot(fit) # dendogram with p values
  ## add rectangles around groups highly supported by the data
  #pvrect(fit, alpha=.95)

  ## Ward Hierarchical Clustering with Bootstrapped p values
  #fit <- pvclust(posdata, method.hclust="ward", method.dist="euclidean")
  #plot(fit) # dendogram with p values
  ## add rectangles around groups highly supported by the data
  #pvrect(fit, alpha=.95)

  ##### Model Based Clustering
  ####library(mclust)
  ####mfit <- Mclust(posdata)
  ####plot(mfit, posdata) # plot results
  ####print(mfit) # display the best model



  dist.methods <- c(
                    #cosine,
                    "correlation"
                    ##"uncentered",
                    ##"abscor",
                    #"euclidean"
                    #"maximum",
                    ##"manhattan",
                    #"canberra",
                    ##"binary",
                    #"minkowski"
                    )
  #####dist.func <- function(x) {
  #####  return (dist(posdata, method=x))
  #####}
  #####dist.all <- lapply(dist.methods, dist.func)

  cluster.methods <- c(
                       "ward"#,
                       #"single",
                       ##"complete",
                       #"average"
                       #"mcquitty",
                       #"median",
                       #"centroid"
                       )

  for (d in dist.methods) {
    for (m in cluster.methods) {
      # suzuki clustering
      print(paste(str(d), m))
      fit <- pvclust(tposdata, method.hclust=m, method.dist=d, nboot=100)
      #fit <- parPvclust(cl, tposdata, method.hclust=m, method.dist=d, nboot=10000)
      plot(fit, main=name) # dendogram with p values
      # add rectangles around groups highly supported by the data
      pvrect(fit, alpha=.95)
      print(fit)
      str(fit)
      seplot(fit)
    }
  }
  
  #####i <- 1
  #####for (d in dist.all) {
  #####  for (m in cluster.methods) {
  #####    # classical clustering
  #####    fit <- hclust(d, method=m)
  #####    plot(fit, main=paste(name, paste(dist.methods[i], m, sep=" x "))) # display dendogram
  #####    groups <- cutree(fit, k=5) # cut tree into 5 clusters
  #####    # draw dendogram with red borders around the 5 clusters
  #####    rect.hclust(fit, k=5, border="red")
  #####  }
  #####  i <- i + 1
  #####}
  
}

significance.filter <- function(x) {
  if (sd(x) > 10 && mean(x) > 5) {
    return (TRUE)
  } else {
    return (FALSE)
  }
}

generate.boxplot <- function(d, mlabel, xlabel, ylabel) {
  n <- ncol(d)
  skip <- 4
  i <- 1
  while (i <= n) {
  #for (i in seq(1, n, skip)) {
    print(i)
    if (i + skip > n) {
      max <- n
      i <- i - 1
    } else {
      max <- i + skip
    }
    #print(i)
    #print(max)
    #print(n)
    #####for (j in i:max) {
    #####  #min <- summary(d[,j])[[2]]
    #####  minv <- boxplot.stats(d[,j])$stats[[1]]
    #####  #max <- summary(d[,j])[[5]]
    #####  maxv <- boxplot.stats(d[,j])$stats[[5]]
    #####  #print(quantile(d[,j]))
    #####  #print(boxplot.stats(d[,j]))
    #####  minout <- which(d[,j] < minv)
    #####  maxout <- which(d[,j] > maxv)
    #####  rnames <- rownames(d)
    #####  #print(colnames(d)[j])
    #####
    #####  #print(paste("min", rnames[minout]))
    #####  #print(paste("max", rnames[maxout]))
    #####}
    #print(max)
    #print(i)
    #print(summary(d[,i:max]))


    #print(significant)
    ####print(ggplot(melt(d[,i:max]), aes(x = variable, y = value)) + xlab(xlabel) + ylab(ylabel) + opts(title = mlabel) + geom_boxplot() + theme_bw())
    #if (length(significant) > 0) {
    print(ggplot(melt(d[,i:max]), aes(x = variable, y = value)) + xlab(xlabel) + ylab(ylabel) + opts(title = mlabel) + geom_boxplot() + theme_bw())
    #}
    if (i + skip >= n) {
      break
    }
    i <- i + skip + 1
  }
}

generate.factoranalysis <- function(d, mlabel, xlabel, ylabel) {
  ev <- eigen(cor(d)) # get eigenvalues
  ap <- parallel(subject=nrow(d),var=ncol(d),rep=100,cent=.05)
  nS <- nScree(ev$values, ap$eigen$qevpea)
  plotnScree(nS)

  #fit <- fa(d, nfactors=7, rotate="promax", fm="ml")
  ###scree.plot(fit$correlations)
  #print(fit, cutoff=0.3) # print results
  #print(str(fit))
  #fa.diagram(fit)
  ##fit <- factor.pa(d, nfactors=3, rotate="varimax")
  ##fit # print results
  
  ## Maximum Likelihood Factor Analysis
  ## entering raw data and extracting 3 factors, 
  ## with varimax rotation 
  #fit <- factanal(d, 5, rotation="varimax")
  #print(fit, digits=2, cutoff=.3, sort=TRUE)
  #load <- fit$loadings 
  #plot(load,type="n") # plot factor 1 by 2 
  #text(load,labels=names(d),cex=.7) # add variable names
}

for (name in basenames) {
  #posdata <- read.table(paste(name, "clusterdata.tsv", sep="-"), header=TRUE, sep="\t", quote="")
  posdata <- read.table(paste(name, ".tsv", sep=""), header=TRUE, sep="\t", quote="")
  posdata <- na.omit(posdata) # listwise deletion of missing
  posdata <- scale(posdata)
  #posdata <- data.frame(posdata[-1], row.names=posdata[[1]], col.names=posdata[,1])
  #tposdata <- as.data.frame(t(posdata))

  #tposdata <- scale(tposdata)
  #posdata <- scale(posdata)

  ##significant <- Filter(significance.filter, posdata)

  #generate.boxplot(significant, "Boxplot", name, "Normalized frequency")
  #generate.factoranalysis(significant, "Boxplot", name, "Normalized frequency")

  batch.cluster(posdata, name)
  #batch.cluster(significant)
  
  print(name)
  #p <- PCA(posdata, ncp=7, graph=FALSE)
  #plot.PCA(p, c(1, 2), new.plot=FALSE, title=paste(name, "による主成分分析", sep=""))
  #plot.PCA(p, c(2, 3), new.plot=FALSE, title=paste(name, "による主成分分析", sep=""))
  #plot.PCA(p, c(2, 4), new.plot=FALSE, title=paste(name, "による主成分分析", sep=""))
  #plot.PCA(p, c(2, 5), new.plot=FALSE, title=paste(name, "による主成分分析", sep=""))
  #plot.PCA(p, c(2, 6), new.plot=FALSE, title=paste(name, "による主成分分析", sep=""))
  #plot.PCA(p, c(2, 7), new.plot=FALSE, title=paste(name, "による主成分分析", sep=""))
  ####print(name)
  #generate.latex(p, name)
  #
  #
  #tp <- PCA(tposdata, graph=FALSE)
  #plot.PCA(tp, c(1, 2), new.plot=FALSE, title=paste(name, "による主成分分析", sep=""))
  #plot.PCA(tp, c(2, 3), new.plot=FALSE, title=paste(name, "による主成分分析", sep=""))
  #plot.PCA(tp, c(2, 4), new.plot=FALSE, title=paste(name, "による主成分分析", sep=""))
  #plot.PCA(tp, c(2, 5), new.plot=FALSE, title=paste(name, "による主成分分析", sep=""))
  #generate.latex(tp, name, append=TRUE)

  
  ##batch.cluster(posdata)
  ##batch.cluster(tposdata)

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

#dev.off()
