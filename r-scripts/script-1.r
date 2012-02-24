A <- read.csv("http://www.cscs.umich.edu/~agong/blog-crawl-results/ParserInspector-BxP.csv")
names(A)
dim(A)

table( A$post_count )
table( A$pct_perfect )
table( A$pct_acceptable )

(A$title + A$date + A$content)/60


A[0<A$pct_acceptable & A$pct_acceptable<1,c(1:12)]



B <- read.csv("http://www.cscs.umich.edu/~agong/blog-crawl-results/ParserInspector-summary-.csv")
names(B)
table(B$best_pct)
x <- B$best_pct==-1
table(B$best_pct)
y <- B$post_count_WordpressParserA[x==TRUE]
y
length(y)
B$blog[x][B$post_count_BlogspotParserA[z]==20]


#[grep("wordpress",B$blog)]

