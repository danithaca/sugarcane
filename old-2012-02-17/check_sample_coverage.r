setwd("~/Dropbox/projects/active/blog_parsers/")

A <- read.table("logs/survey_respondents.txt")
a <- as.character(A$V1)

B <- read.table("blogCrawler/logs/crawl_b/complete.txt", nrows=859)
b <- unlist(lapply( strsplit(as.character(B$V6),"/"), function(x){ tail( x, n=1)} ))

head(a)
head(b)

table( a %in% b )
table( b %in% a )

b[b%in%a]

#I don't know where this list came from
# -- they seem to be political blogs --
#but they have almost nothing in common with the survey respondents'