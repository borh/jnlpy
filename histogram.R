cairo_pdf(file="adverb-modality-histogram.pdf", onefile=TRUE, pointsize=6)#, family="Japan1", pointsize=8, onefile=TRUE)

worktitle <- "Average distances between adverbs and modal forms"
#worktitle <- "Average sentence length"

basenames <- c("Yahoo!知恵袋", "検定教科書", "生産実態新聞", "生産実態雑誌", "非母集団ベストセラー", "Yahoo!ブログ", "国会会議録", "流通実態書籍",  "生産実態書籍", "白書")
files <- as.vector(lapply(basenames, paste, "-adverb-modality-distance.tsv", sep=""))
#files <- as.vector(lapply(basenames, paste, "-sentence-length.tsv", sep=""))

#files <- c()
#
#for (file in basefiles) {
#  append(files, paste(as.character(file), "-sentence-length.tsv", sep=""))
#}

source("normalize.R")

get.data <- function(fs) {
  return(lapply(fs, read.table, header=TRUE))
}

data <- get.data(files)

new <- list()

get.lengths <- function(x) {
  r <- as.data.frame(x)
  ret <- c()
  for (el in r[-1]) {
    ret <- c(ret, el[el<80])
  }

                                        #  r <- as.data.frame(x)$文の長さ.形態素.
                                        #return(r[r<60])
  return(ret)
}

new <- lapply(data, get.lengths)

smallest <- get.smallest.number.of.samples(new)

factors <- get.factors(new, smallest)

#x <- lapply(new, normalize, n=factors)

#for (d in data) {
#  print(d)
#  append(new, normalize(as.data.frame(d)$文の長さ.形態素.))
#}

#new <- list(normalize(as.data.frame(data[1])$文の長さ.形態素.), normalize(as.data.frame(data[2])$文の長さ.形態素.))

#library("plotrix")

library("plotrix")
library("graphics")

library("RColorBrewer")
mycolors <- brewer.pal(10, "Paired")

#multhist(new, main=paste(worktitle, "all subcorpora"))
#legend(-0.5, -0.5, files, col=2:12, pch=1:10, lty=1, merge=TRUE)

mybreaks <- c(0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80)
myaverages <- hist(new[[1]], breaks=mybreaks, plot=FALSE)$mids
left <- myaverages - 2.5
right <- myaverages + 2.5
mylabels <- c()
for (i in 1:length(left)) {
  mylabels <- c(mylabels, paste(left[i], right[i], sep="-"))
}
print(left)
print(mylabels)

sampledist <- matrix(c(normalize(hist(new[[1]], breaks=mybreaks, plot=FALSE)$count)))

for (i in 2:length(new)) {
  sampledist <- cbind(sampledist, c(normalize(hist(new[[i]], breaks=mybreaks, plot=FALSE)$count)))
  #h$i <- hist(new[[i]], breaks=mybreaks, plot=FALSE)$count
}

print(sampledist)

barplot(t(sampledist), beside=TRUE, names.arg=mylabels, legend.text=basenames, axis.lty=1, col=mycolors, xlab=worktitle, ylab="Samples (ratio)", main=paste(worktitle, "in all subcorpora"))

for (i in 1:length(new)) {
  hist(new[[i]], breaks=mybreaks, main=paste(worktitle, basenames[i], sep=" in "), ylab="Samples", xlab=worktitle)
  #hist(new[[i]], breaks=12)
  #print(h)
  #h$counts <- h$counts/factors[i]
  #hist(h)
}

for (i in 1:length(data)) {
  j <- 1
  #plot.new()
  plot.default(0, xlim=c(0, 80), ylim=c(0, 0.2), main=paste(basenames[i], paste(": Histogram of", cnames[j])), xlab="Observed distance", ylab="Occurrence frequency")
  cnames <- colnames(data[[i]][-1])
  lcolors <- rainbow(length(cnames))
  legend(40, 0.2, legend=cnames, col=lcolors)
  for (combination in data[[i]][-1]) { # data[[i]]->corpus, first elem. is sample name, remove
    notna <- as.vector(na.omit(combination[-1])) #lapply(combination, na.omit)
    notna <- Filter(function(x) x < 80, notna)
    if (length(notna) > 15) {
      averagev <- sum(notna) / length(notna)
                                        #print (notna)
                                        #print (averagev)
      #print (combination)
      h <- hist(notna, breaks=mybreaks, freq=FALSE, main=paste(basenames[i], paste(": Histogram of", cnames[j])), xlab="Observed distance", ylab="Occurrence frequency", plot=FALSE)
      lines(h$mids, h$density, col=lcolors[j])
    }
    j <- j + 1
  }
}

dev.off()
