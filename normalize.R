get.smallest.number.of.samples <- function(samples) {
  lengths <- lapply(samples, length)
  m <- 8000000
  for (l in lengths) {
    #print(l)
    if (l < m) {
      m <- l
    }
  }
  return(m)
}

get.factors <- function(xs=xs, n=n) {
  lengths <- lapply(xs, length)
  factors <- c()
  for (l in lengths) {
    factors <- c(factors, l/n)
  }
  return(factors)
}

normalize <- function(x) {
  d <- as.vector(x, mode="numeric")
  return(d/sum(d))
}
