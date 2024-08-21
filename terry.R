cairo_pdf(file="2010-writing-systems-report.pdf", onefile=TRUE, pointsize=8, width = 8, height = 4)#, family="Japan1", pointsize=8, onefile=TRUE)
#png(filename = "2010-writing-systems-report.png",
png(
    width = 1200, height = 600, units = "px",
    pointsize = 16, bg = "white",
    type = "cairo")

basenames <- c(
#"名詞",
#"動詞",
#"副詞",
#"形容詞"
"nouns",
"verbs",
"adverbs",
"adjectives(-i)"
)

#library("pvclust")
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
                    cosine#,
                    #"correlation",
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
      fit <- pvclust(tposdata, method.hclust=m, method.dist=d, nboot=10000)
      #fit <- parPvclust(cl, tposdata, method.hclust=m, method.dist=d, nboot=10000)
      plot(fit, main=name) # dendogram with p values
      # add rectangles around groups highly supported by the data
      pvrect(fit, alpha=.95)
      print(fit)
      seplot(fit)
    }
  }
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
    print(ggplot(melt(d[,i:max]), aes(x = variable, y = value)) + xlab(xlabel) + ylab(ylabel) + opts(title = mlabel) + geom_boxplot() + theme_bw())
    #}
    if (i + skip >= n) {
      break
    }
    i <- i + skip + 1
  }
}

cummulative.frequency <- function(xs) {
    total <- sum(xs)
    return (cumsum(xs) / total)
}

read.tsv.files <- function(basename) {
    x <- data.frame(
        pos = basename,
        rank = read.table(paste("lemma-orth-relations-rank-", basename, ".tsv", sep=""), header=TRUE, sep="\t", quote="")
    )
    x$rank.order <- order(x$rank.frequency, decreasing=TRUE)
    x$rank.frequency <- x$rank.frequency[x$rank.order]
    x$rank.cummulative.frequency <- cummulative.frequency(x$rank.frequency)
    x$rank.lemma <- x$rank.lemma[x$rank.order]
    x$rank.variations <- x$rank.variations[x$rank.order]
    x$rank.variation.type <- x$rank.variation.type[x$rank.order]
    return (x)
}

read.spc.files <- function(basename) {
    tfl <- read.tfl(paste("type-frequency-", basename, ".tfl", sep=""))
    spc <- tfl2spc(tfl)
    return (list(spc, basename))
    print (str(spc))
    #x$tfl <- tfl
    #print (str(x))
    x <- cbind(x, spc)
    print (str(x))
}

generate.models <- function(spc, name) {
# Zipf-Mandelbrot model
    spc.fzm <- lnre("fzm", spc, exact=FALSE)
    spc.fzm.spc <- lnre.spc(spc.fzm, N(spc.fzm))
    spc.fzm.vgc <- lnre.vgc(spc.fzm, (1:100)*28e+3)
    print("models generated")
    return (data.frame(name = name,
                       spc = spc,
                       spc.fzm = spc.fzm,
                       spc.fzm.spc = spc.fzm.spc,
                       spc.fzm.vgc = spc.fzm.vgc))
}

#library(lattice)

find.frequency.index <- function(x, index) {
    i <- 1
    for (freq in x) {
        if (freq <= index) {
            return (i)
        }
        i <- i + 1
    }
}

filter.by.condition <- function(d, sup, c) {
    rx <- c()
    ry <- c()
    i <- 1
    for (value in d) {
        if (value==c) {
            rx <- c(rx, i)
            ry <- c(ry, sup[i])
        }
        i <- i + 1
    }
    return (list(rx, ry))
}

plot.distributions <- function(x) {
# Plot of rank-variations
    par(mfrow=c(2,2))
    print(str(x))
    plot(x$rank.variations, type="p", main=x$pos[1], xlab="Lemma frequency rank", ylab="Number of orthbase variations per lemma")
    quarter <- Position(function(z) {z >= 0.9}, x$rank.cummulative.frequency)
    lines(approx(x$rank.variations), col = 2, pch = "*")
    #lines(approx(x$rank.variations, method = "constant"), col = 3, pch = "*")
    #lines(spline(x$rank.variations, n=80), col = 4)
    #lines(spline(x$rank.variations, n=80, method = "natural"), col = 3)
    #lines(spline(x$rank.variations, n=20, method = "periodic"), col = 4)
    legend(length(x$rank.variations)*0.35,max(x$rank.variations)*.85, c("linear interpolation"), col=2, lty=1)

    print(quarter)
    hl <- find.frequency.index(x$rank.frequency, 1)
    #third.quartile <- summary(x$rank.frequency)[[5]]
    #first.quartile <- summary(x$rank.frequency)[[2]]
    print (summary(x$rank.frequency))
    #third.quartile.index <- find.frequency.index(x, third.quartile)
    #first.quartile.index <- find.frequency.index(x, first.quartile)
    abline(v=hl, col=3, lty=2)
    text(hl, max(x$rank.variations)*.7, c("hapax\nlegema ->"), pos=4, col=3)
    abline(v=quarter, col=4, lty=2)
    text(quarter, max(x$rank.variations)*.7, c("90% cumm.\nfrequency"), pos=1, col=4)
    #abline(v=third.quartile.index, col="blue")
    #abline(v=first.quartile.index, col="green")
    ################################################plot(x$rank.frequency[1:quarter], type="l", xlab="Lemma rank", ylab="Frequency", main=paste("Lemma rank frequency of ", x$pos[1]), sub=" (up to 90% cummulative frequency only)")
    #abline(v=hl, col="red")
    #abline(v=third.quartile.index, col="blue")
    #abline(v=first.quartile.index, col="green")

    #plot(density(x$rank.frequency[x$rank.order][1:third.quartile.index]))
    #hist(x$rank.frequency[x$rank.order][1:third.quartile.index])
    #plot(density(t(x$rank.variations[x$rank.order])))
    ############for (type in c("0.9 > ... > 0.8", "0.8 > ... > 0.7", "0.7 > ... > 0.6", "0.6 > ... > 0.5", "<0.5")) {
    ############    #print (type)
    ############    #print (hl)
    ############    #print (third.quartile.index)
    ############    #print (first.quartile.index)
    ############    #plot(x$rank.variations[x$rank.variation.type==type][1:length(x$rank.variations)], type="p", main=x$pos[1])
    ############    data <- filter.by.condition(x$rank.variation.type, x$rank.variations, type)
    ############    #print (str(data))
    ############    #print (data)
    ############    plot(data[[1]], data[[2]], xlim=c(1,length(x$rank.variations)), type="p", pch=19, main=paste(x$pos[1], type, sep=" with distribution of type "), xlab="lemma rank frequency", ylab="number of ortho-base variations")
    ############    print("boo")
    ############    abline(v=hl, col="red")
    ############    abline(v=third.quartile.index, col="blue")
    ############    abline(v=first.quartile.index, col="green")
    ############}
    #plot(x$rank.variations[x$rank.order][x$rank.variation.type=="extreme"][1:length(x$rank.variations)], type="p", main=x$pos[1])
    #abline(v=hl, col="red")
    #plot(x$rank.variations[x$rank.order][x$rank.variation.type=="skewed"][1:length(x$rank.variations)], type="p", main=x$pos[1])
    #abline(v=hl, col="red")
    #plot(x$rank.variations[x$rank.order][x$rank.variation.type=="split"][1:length(x$rank.variations)], type="p", main=x$pos[1])
    #abline(v=hl, col="red")
    table(t(x$rank.variations), c(1:length(x$rank.variations)))
    barplot(table(x$rank.variations), beside=TRUE, axis.lty=1, xlab="Number of variations", ylab="Number of lemmas", main=paste("Distribution of lemma-orthbase variation in", x$pos[1]))
    barplot(table(x$rank.variations[1:hl]), beside=TRUE, axis.lty=1, xlab="Number of variations", ylab="Number of lemmas", main=paste("Distribution of lemma-orthbase variation in", x$pos[1]), sub="(without hapax legema)")
    barplot(table(x$rank.variations[1:quarter]), beside=TRUE, axis.lty=1, xlab="Number of variations", ylab="Number of lemmas", main=paste("Distribution of lemma-orthbase variation in", x$pos[1]), sub="(up to 90% cumm. frequency)")
    barplot(table(x$rank.variations[1:100]), beside=TRUE, axis.lty=1, xlab="Number of variations", ylab="Number of lemmas", main=paste("Distribution of lemma-orthbase variation in", x$pos[1]), sub="(most frequent 100 lemmas only)")
    #ten <- length(x$rank.variations)*.1
    #print("ten")
    #print(ten)
    #barplot(table(x$rank.variations[1:as.integer(length(x$rank.variations)*0.05)]), beside=TRUE, axis.lty=0, xlab="Number of variations", ylab="Number of lemmas", main=paste("Distribution of lemma-orthbase variation in", x$pos[1]), sub="(10% of lemmas only)")


    #plot(x$rank.variations[x$rank.order[x$rank.variation.type=="split"][1:1000]], type="l", main=x$pos[1])
    #lines(x$rank.variations[x$rank.order[x$rank.variation.type=="skewed"][1:1000]], type="l", col="red")
    #lines(x$rank.variations[x$rank.order[x$rank.variation.type=="extreme"][1:1000]], type="l", col="blue")
    #variations.f <- factor(x$rank.variation.type, levels=c(1,2,3), labels=c("split","skewed","extreme"))
    #densityplot(~x$rank.frequency[x$rank.order]|variations.f, data=x, main="Density Plot by Variation Dist. Type", xlab="Rank")
    #densityplot(~x$rank.frequency[x$rank.order]|variations.f, data=x, main="Density Plot by Variation Dist. Type", xlab="Rank", layout=c(1,3))

    print(x$pos[1])
    print (cor.test(x$rank.variations, x$rank.frequency))
    print (cor.test(x$rank.variations, x$rank.frequency, alternative="less"))
    #print (cor.test(x$rank.variations[x$rank.order], x$rank.frequency[x$rank.order], method="spearman"))
    #extreme <- x$rank.variation.type[x$rank.variation.type=="extreme"]
    #plot(extreme[x$rank.order], type="l", main=x$pos[1])
}

plot.models <- function(xs) {
    for (x in xs) {
        # Type frequency spectrum plots
        plot(x$spc, main=paste("Frequency Spectrum of ", x$name, sep=""))
        plot(x$spc, log="x", main=paste("Frequency Spectrum of ", x$name, sep=""))
        # Zipf-Mandelbrot model plot
        plot(x$spc, x$fzm.spc, legend=c("observed", "fZM"))
    }
}

plot.zipf <- function(x) {
    # Type frequency spectrum plots
    print(x)
    plot(x[[1]], main=paste("Frequency Spectrum of ", x[[2]], sep=""))
    plot(x[[1]], log="x", main=paste("Frequency Spectrum of ", x[[2]], sep=""))
}

data.tsv <- as.list(lapply(basenames, read.tsv.files))
#data.spc <- as.list(lapply(basenames, read.spc.files))

#######library("ggplot2")
#######
#######bincounts <- lapply(data.tsv, function(x) { n <- x$pos[1]; return (table(x$rank.variations[1:100], dnn="variations")) })
#######xbincounts <- lapply(data.tsv, function(x) { n <- x$pos[1]; return (xtabs(rank.variations[1:100] ~ max(rank.variations[1:100]), data=x)) })
########bincounts <- lapply(data.tsv, function(x) { return (table(x$rank.variations[1:100]) / sum(x$rank.variations[1:100])) })
#######
########ggplot(as.data.frame(data.tsv), aes(x=x$rank.variations)) + stat_bin()
#######str(bincounts)
#######summary(bincounts)
#######str(melt(bincounts))
#######maxvars <- 1
#######for (x in bincounts) {
#######    m <- max(bincounts$Var.1)
#######    if (m > maxvars) {
#######        maxvars <- m
#######    }
#######}
#######
#######custom.merge <- function(xs) {
#######    maxcat <- 1
#######    for (x in xs) {
#######        
#######        print (str(x))
#######        print(x)
#######    }
#######
#######}
#######
#######custom.merge(xbincounts)
#######
#######print(bincounts)
#######print(melt(bincounts))
#######print(rbind(nouns=bincounts[[1]], verbs=bincounts[[2]], adverbs=bincounts[[3]], adjectives=bincounts[[4]]))
#######print(melt(bincounts, id=1:4, na.rm=FALSE, names=c("nouns", "verbs", "adverbs", "adjectives")))
#######print(rbind.fill(bincounts))
#######print(merge(nouns=bincounts[[1]], verbs=bincounts[[2]], adverbs=bincounts[[3]], adjectives=bincounts[[4]], by=c("nouns"), all=TRUE))
#######ggplot(melt(bincounts), aes(x=L1, y=Var.1)) + geom_bar()


par(mfrow=c(2,2))
par(mar=c(3,3,2,1))

#barplot(lapply(x$rank.variations[1:100], table), beside=TRUE, axis.lty=0, xlab="Number of variations", ylab="Number of lemmas", main="Orthographic variation (100 most frequent lemmas)")
for (x in data.tsv) {
    xlimit <- Position(function(z) {z >= 0.9}, x$rank.cummulative.frequency)
    sub <- "(90% cummulative frequency)"
    barplot(table(x$rank.variations[1:xlimit]), axis.lty=0, xlab="Number of variations", ylab="Number of lemmas")
    #barplot(table(x$rank.variations[1:xlimit])[1:22], axis.lty=0, xlab="Number of variations", ylab="Number of lemmas", main=paste("Orthographic variation in", x$pos[1]), sub=sub)
    text(length(table(x$rank.variations[1:xlimit]))*.75, max(table(x$rank.variations[1:xlimit]))*.8, x$pos[1], cex=2.4)
    text(length(table(x$rank.variations[1:xlimit]))*.75, max(table(x$rank.variations[1:xlimit]))*.65, paste("\nrange = ", as.integer(summary(x$rank.variations[1:xlimit])[[1]]), "-", as.integer(summary(x$rank.variations[1:xlimit])[[6]]), "\nmean = ", summary(x$rank.variations[1:xlimit])[[4]], sep=""), cex=1.8)
    print(x$pos[1])
    print(table(x$rank.variations[1:xlimit]))
    print(summary(x$rank.variations[1:xlimit]))
    print(summary(x$rank.variations))
}
for (x in data.tsv) {
    xlimit <- 100
    sub <- "(100 most frequent lemmas)"
    barplot(table(x$rank.variations[1:xlimit]), axis.lty=0, xlab="Number of variations", ylab="Number of lemmas")
    text(length(table(x$rank.variations[1:xlimit]))*.75, max(table(x$rank.variations[1:xlimit]))*.8, x$pos[1], cex=2.4)
    text(length(table(x$rank.variations[1:xlimit]))*.75, max(table(x$rank.variations[1:xlimit]))*.65, paste("\nrange = ", as.integer(summary(x$rank.variations[1:xlimit])[[1]]), "-", as.integer(summary(x$rank.variations[1:xlimit])[[6]]), "\nmean = ", summary(x$rank.variations[1:xlimit])[[4]], sep=""), cex=1.8)
    print(x$pos[1])
    print(summary(x$rank.variations[1:xlimit]))
}
quit()
#print (str(data.tsv))
#print (str(data.spc))

lapply(data.tsv, plot.distributions)
#lapply(data.spc, plot.zipf)

#models <- lapply(data.spc, generate.models)

#plot.models(models)
#####warnings()
#for (name in basenames) {
#  posdata <- read.table(paste("lemma-orth-relations-rank-", name, ".tsv", sep=""), header=TRUE, sep="\t", quote="")
#  print(name)
#
#  posdata$rank.order <- order(posdata$frequency, decreasing=TRUE)
#  plot(posdata$variations[posdata$rank.order[1:1000]], type="l", main=name)
#  #hist(posdata$variations[posdata$variations < 20])
#  #hist(posdata$frequency)
#  print(summary(posdata))
#
#  posdata.tfl <- read.tfl(paste("type-frequency-", name, ".tfl", sep=""))
#  posdata.spc <- tfl2spc(posdata.tfl)
#
#  #posdata.bin.vgc <- vgc.interp(posdata.spc, N(posdata.emp.vgc), m.max=1)
#
#  plot(posdata.spc, main=paste("Frequency Spectrum of ", name, sep=""))
#  plot(posdata.spc, log="x", main=paste("Frequency Spectrum of ", name, sep=""))
#  plot.default(posdata.spc, main=paste("Frequency Spectrum of ", name, sep=""))
#
#  posdata.fzm <- lnre("fzm", posdata.spc, exact=FALSE)
#  posdata.fzm.spc <- lnre.spc(posdata.fzm, N(posdata.fzm))
#  plot(posdata.spc, posdata.fzm.spc, legend=c("observed","fZM"))
#  posdata.fzm.vgc <- lnre.vgc(posdata.fzm, (1:100)*28e+3)
#
#}
dev.off()
