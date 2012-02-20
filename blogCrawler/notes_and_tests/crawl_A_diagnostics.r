A <- read.csv("~/Desktop/temp.csv", header=F)
dim(A)
names(A) <- c("url","start","end")

A$start <- as.POSIXct(A$start)
A$end <- as.POSIXct(A$end)

plot( A$end )

A$end - A$start
summary(A$end - A$start)
A$elapsed <- as.vector(A$end - A$start)
summary(A$elapsed)
plot( density(A$elapsed) )
plot( A$elapsed, A$start )

table( A$elapsed < 5, A$start < as.POSIXct("2012-01-05 12:04:20") )

table( A$elapsed == 0 )
#227 "loaded" in zero sec

table( A$elapsed > 0 & A$elapsed < 5 )
#336 "loaded" 0 < x < 5 sec

A$url[A$elapsed > 0 & A$elapsed < 5]

#303 Have entries...

227+336+303

dim(A)

#657 have "read-only" filesystem

plot( density( A$elapsed[A$elapsed > 5] ) )

A[A$elapsed > 5,c("url","elapsed")]

plot( A$start, log(1+A$elapsed) )

x <- as.POSIXct("2012-01-06 02:40:00"); abline(v=x)

Y <- A$elapsed[A$start<x]/60
summary( Y )
table( Y > 12*60 )
barplot(table( trunc(Y/60) )/length(Y), )
