#read.table(file, header = FALSE, sep = "", quote = "\"'",
#                dec = ".", row.names, col.names,
#                as.is = !stringsAsFactors,
#                na.strings = "NA", colClasses = NA, nrows = -1,
#                skip = 0, check.names = TRUE, fill = !blank.lines.skip,
#                strip.white = FALSE, blank.lines.skip = TRUE,
#                comment.char = "#",
#                allowEscapes = FALSE, flush = FALSE,
#                stringsAsFactors = default.stringsAsFactors(),
#                fileEncoding = "", encoding = "unknown")

scale.rows <- function(x,s) {
  return(apply(x,2,function(x){x*s}))
}

div.by.sum <- function(x) {
  scale.rows(x,1/(rowSums(x)+1e-16))
}

do.mds <- function(filename) {
  dataFrame <- read.table(file=filename, header=TRUE, dec = ".", sep="\t", comment.char="", allowEscapes=TRUE)
  labels <- dataFrame[,1] # row labels
  c <- colnames(dataFrame)[-1]
  #c <- c[-1]
  data <- as.matrix(dataFrame[-1], nrow=length(labels), ncol=length(c), dimnames=list(as.vector(labels), as.vector(c)))
  normd <- div.by.sum(data)
                                        # Classical MDS
                                        # N rows (objects) x p columns (variables)
                                        # each row identified by a unique row name
  #d <- dist(data) # euclidean distances between the rows
  d <- dist(normd) # euclidean distances between the rows
  fit <- cmdscale(d, eig=TRUE, k=2) # k is the number of dim
  x <- fit$points[,1]
  y <- fit$points[,2]
  return (list(x=x, y=y, labels=labels, filename=filename))
}

draw.plot.with.title <- function(x, y, labels, title="", color="red") {
  plot(x,
       y,
       xlab="次元1",
       ylab="次元2",
       main=paste(title, "多次元尺度構成法による配置図", sep=""),
       type="n")
  text(x, y, labels=labels, cex=.7, col=color)
}

draw.points.on.existing.graph <- function(x, y, color="red", pch=".") {
  points(x, y, col=color, pch=pch)
}

auto.draw.multiple.datasets <- function(datasets) {
  color.index <- 1
  colors <- rainbow(length(datasets) + 1)
  # find the largest x na y position from all the graphs
  maxx <- 0
  maxy <- 0
  for (data in datasets) {
    if (maxx < max(data$x)) {
        maxx <- max(data$x)
    }
    if (maxy < max(data$y)) {
        maxy <- max(data$y)
    }
  }
  # draw empty big graph
  plot (c(0),
        c(0),
        xlab="次元1",
        ylab="次元2",
        main="モダリティ形式を素材にした多次元尺度構成法による配置図",
        type="n",
        ylim=c(-maxy-0.1,maxy+0.1),
        xlim=c(-maxx-0.1,maxx+0.1))
  for (data in datasets) {
    #draw.points.on.existing.graph(x=data$x, y=data$y, color=colors[color.index], pch=color.index)
    draw.points.on.existing.graph(x=data$x, y=data$y, color=colors[color.index], pch=".")
    color.index <- color.index + 1
  }
  labels <- c()
  for (data in datasets) {
    labels <- c(data$filename, labels)
  }
  legend(-maxx, -maxy+0.4, labels, cex=0.8, col=colors, pch=".", lty=1:2)
  #legend(-maxx, maxy, labels, cex=0.8, col=colors, pch=1:18, lty=1:2)
}


#pdf(file = paste("corpora-all", "pdf", sep="."), family="Japan1Ryumin")
#
#bccwj.goshu <- do.mds("corpora-goshu.tsv")
#draw.plot.with.title(bccwj.goshu$x, bccwj.goshu$y, bccwj.goshu$labels, "語種を素材に使用した", "blue")
#bccwj.writing <- do.mds("corpora-writing.tsv")
#draw.plot.with.title(bccwj.writing$x, bccwj.writing$y, bccwj.writing$labels, "字種を素材に使用した", "blue")
#bccwj.pos <- do.mds("corpora-pos.tsv")
#draw.plot.with.title(bccwj.pos$x, bccwj.pos$y, bccwj.pos$labels, "品詞を素材に使用した", "blue")
#bccwj.adverbs <- do.mds("corpora-adverbs.tsv")
#draw.plot.with.title(bccwj.adverbs$x, bccwj.adverbs$y, bccwj.adverbs$labels, "推量副詞を素材に使用した", "blue")
#bccwj.modality <- do.mds("corpora-modality.tsv")
#draw.plot.with.title(bccwj.modality$x, bccwj.modality$y, bccwj.modality$labels, "モダリティを素材に使用した", "blue")
#bccwj.adverb.modality <- do.mds("corpora-adverb-modality.tsv")
#draw.plot.with.title(bccwj.adverb.modality$x, bccwj.adverb.modality$y, bccwj.adverb.modality$labels, "推量副詞とモダリティを素材に使用した", "blue")


pdf(file = paste("modality-all", "pdf", sep="."), family="Japan1Ryumin")

datasets <- list(
do.mds("検定教科書-OT-modality.tsv"),    do.mds("白書-OW-modality.tsv"),
#do.mds("Yahoo!知恵袋-OC-modality.tsv"),  do.mds("検定教科書-OT-modality.tsv"),    do.mds("生産実態SC・書籍-PB-modality.tsv"),  do.mds("白書-OW-modality.tsv"),
#do.mds("Yahoo!ブログ-OY-modality.tsv"),  do.mds("国会会議録-OM-modality.tsv"),    do.mds("流通実態SC・書籍-LB-modality.tsv"),  do.mds("生産実態SC・新聞-PN-modality.tsv"),         do.mds("生産実態SC・雑誌-PM-modality.tsv"),  do.mds("非母集団SC・ベストセラー-OB-modality.tsv"))
do.mds("国会会議録-OM-modality.tsv"),    do.mds("生産実態SC・新聞-PN-modality.tsv"),         do.mds("生産実態SC・雑誌-PM-modality.tsv"),  do.mds("非母集団SC・ベストセラー-OB-modality.tsv"))

datasets <- list(read.scaled())

auto.draw.multiple.datasets(datasets)

#ot.modality <- do.mds("検定教科書-modality.tsv")
#draw.plot.with.title(ot.modality$x, ot.modality$y, ot.modality$labels, "モダリティを素材に使用した", "blue")
#
#
#pn.modality <- do.mds("新聞-modality.tsv")
#draw.points.on.existing.graph(pn.modality$x, pn.modality$y, "red")



#goshu.filenames = list(
##  "Yahoo!ブログ-OY-goshu.tsv",
##  "Yahoo!知恵袋-OC-goshu.tsv",
#  "国会会議録-OM-goshu.tsv",
#  "検定教科書-OT-goshu.tsv"
##  "流通実態SC・書籍-LB-goshu.tsv"
##  "生産実態SC・新聞-PN-goshu.tsv",
##  "生産実態SC・書籍-PB-goshu.tsv",
##  "生産実態SC・雑誌-PM-goshu.tsv",
##  "白書-OW-goshu.tsv",
##  "非母集団SC・ベストセラー-OB-goshu.tsv"
#  )
#
#goshu.dataset <- lapply(goshu.filenames, do.mds)
#auto.draw.multiple.datasets(goshu.dataset)

#
#
#pn.goshu <- do.mds("生産実態SC・新聞-PN-goshu.tsv")
#draw.points.on.existing.graph(pn.goshu$x, pn.goshu$y)
#
#ow.goshu <- do.mds("白書-OW-goshu.tsv")
#draw.points.on.existing.graph(ow.goshu$x, ow.goshu$y, "green")




#do.mds("corpora-goshu.tsv", "語種を素材に使用した")
#do.mds("corpora-writing.tsv", "字種を素材に使用した")
#do.mds("corpora-pos.tsv", "品詞を素材に使用した")
##do.mds("corpora-types.tsv", "異なり語彙素を素材に使用した")
#do.mds("corpora-modality.tsv", "モダリティ形式を素材に使用した")
#do.mds("corpora-adverbs.tsv", "推量副詞を素材に使用した")
#do.mds("corpora-adverb-modality.tsv", "副詞とモダリティ形式を素材に使用した")
#
#dev.off()
#
#
#pdf(file = paste("files-検定", "pdf", sep="."), family="Japan1Ryumin")
#
#do.mds("検定教科書-pos.tsv", "品詞を素材に使用した")

dev.off()

#dataFrame <- read.table(file="mds-corpora-modality.tsv", header=TRUE, dec = ".", sep="\t")
#
##dataFrame <- read.delim2(file="bccwj-pos-all.tsv", header=TRUE)
#
#r <- dataFrame[,1]
#c <- colnames(dataFrame)
#c <- c[-1]
#
#data <- as.matrix(dataFrame[-1], nrow=length(r), ncol=length(c), dimnames=list(as.vector(r), as.vector(c)))
#
##r <- dataFrame[,1]
##c <- colnames(dataFrame)
##c <- c[-1]
##
##data <- matrix(data=dataFrame[,-1], nrow=length(r), ncol=length(c), dimnames=list(as.vector(r), as.vector(c))) # minus the corpus and file names
##
#scale.rows <- function(x,s) {
#	return(apply(x,2,function(x){x*s}))
#}
#
#div.by.sum <- function(x) {
#  scale.rows(x,1/(rowSums(x)+1e-16))
#}
#
#normd <- div.by.sum(data)
##normd <- normd*100
#
## Classical MDS
## N rows (objects) x p columns (variables)
## each row identified by a unique row name
#
#d <- dist(normd) # euclidean distances between the rows
#fit <- cmdscale(d, k=2) # k is the number of dim
##fit <- cmdscale(d, eig=TRUE, k=2) # k is the number of dim
##fit # view results
#
## plot solution
##x <- fit[,1]
##y <- -fit[,2]
##x <- fit$points[,1]
##y <- fit$points[,2]
#
#pdf(file = "bccwj-metric-modality-mds.pdf", family="Japan1Ryumin")
#
##plot(x, y, xlab="Coordinate 1", ylab="Coordinate 2",
#plot(fit, xlab="次元1", ylab="次元2",
#  main="副詞とモダリティ形式を素材に使用した多次元尺度構成法による配置図", type="n")
##text(x, y, labels = r, cex=.7)
#text(fit, labels = r, cex=.7, col="red")
#
#dev.off()
#
#pdf(file = "bccwj-mds-modality.pdf", family="Japan1Ryumin")
## Ward Hierarchical Clustering with Bootstrapped p values
#library(pvclust)
#tdata <- as.matrix(t(normd), nrow=length(c), ncol=length(r), dimnames=list(as.vector(c), as.vector(r)));
#fit <- pvclust(tdata, method.hclust="ward",
#               method.dist="euclidean")
#plot(fit) # dendogram with p values
## add rectangles around groups highly supported by the data
#pvrect(fit, alpha=.95)
#
#dev.off()
#
### Model Based Clustering
##library(mclust)
##cfit <- Mclust(normd)
##plot(cfit, normd) # plot results 
##print(cfit) # display the best model
#
### K-Means Clustering with 5 clusters
##clusterfit <- kmeans(normd, 5)
##
### Cluster Plot against 1st 2 principal components
##
### vary parameters for most readable graph
##library(cluster)
##clusplot(normd, clusterfit$cluster, color=TRUE, shade=TRUE, 
##  	 labels=2, lines=0)
##
### Centroid Plot against 1st 2 discriminant functions
##library(fpc)
##plotcluster(normd, clusterfit$cluster)
