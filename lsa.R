#d1 <- read.table("bccwj-modality.tsv", header=TRUE)
#d2 <- read.table("bccwj-adverbs.tsv", header=TRUE)
#
##determine.color <- function(x) {
##    if (which(d == x) > 0) {
##        return 1
##    }
##
##}
#
#filenames <- d1[[1]]
#
#d1 <- data.frame(d1[-1], row.names=filenames)
#d2 <- data.frame(d2[-1], row.names=filenames)
#
#total <- cbind(d1, d2)
#pdf(file="lsa.pdf", family="Japan1", pointsize=8, onefile=TRUE)
cairo_pdf(file="lsa.pdf", onefile=TRUE, pointsize=11)#, family="Japan1", pointsize=8, onefile=TRUE)

total <- read.table("corpora-adverb-modality-distance.tsv-", header=TRUE)
total <- data.frame(total[-1], row.names=total[[1]])

#library("plotrix")

#library("lsa")
#l <- lsa(total, 2)

#plot(l$tk)
#text(l$tk, labels=rownames(total))

library("FactoMineR")
p <- PCA(total, graph=FALSE)
plot.PCA(p, new.plot=FALSE, title="モダリティ形式によるBCCWJの主成分分析")
#plot.PCA(p, new.plot=FALSE, title="副詞によるBCCWJの主成分分析", palette=palette(rainbow(30)), habillage="ind")

#library("MASS")
#swiss.x <- as.matrix(swiss[, -1])
#total.dist <- dist(total)
#total.mds <- isoMDS(total.dist)
#plot(total.mds$points, type = "n")
#text(total.mds$points, labels = as.character(1:nrow(total)))
#total.sh <- Shepard(total.dist, total.mds$points)
#plot(total.sh, pch = ".")
#lines(total.sh$x, total.sh$yf, type = "S")

#embedFonts("lsa.pdf", fontpaths="/usr/share/fonts/takao-fonts")

## K-Means Clustering with 5 clusters
#fit <- kmeans(total, 5)
#
## Cluster Plot against 1st 2 principal components
#
## vary parameters for most readable graph
#library(cluster)
#clusplot(total, fit$cluster, color=TRUE, shade=TRUE,
#   labels=2, lines=0)
#
## Centroid Plot against 1st 2 discriminant functions
#library(fpc)
#plotcluster(total, fit$cluster)

dev.off()
