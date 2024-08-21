cairo_pdf(file="advmod-dist-histogram.pdf", onefile=TRUE, pointsize=6)#, family="Japan1", pointsize=8, onefile=TRUE)

worktitle <- "Average distances between adverbs and modal forms"
#worktitle <- "Average sentence length"

basenames <- c("Yahoo!知恵袋", "検定教科書", "生産実態新聞", "生産実態雑誌", "非母集団ベストセラー", "Yahoo!ブログ", "国会会議録", "流通実態書籍",  "生産実態書籍", "白書")
basefiles <- as.vector(lapply(basenames, paste, "-sbins_advmod_dist.tsv", sep=""))

files <- c()

for (file in basefiles) {
  sequence = 4:8
  for (i in sequence) {
    files <- c(files, paste(paste(file, i, sep="-"), "tsv", sep="."))
  }
}

get.data <- function(fs) {
  return(lapply(fs, read.csv2, header=TRUE, sep="\t"))
}

data <- get.data(files)

