A <- read.csv("map-test-1.csv")
dim(A)
names(A)

names(A[,c(4:8)])
B <- A[,grep("Parser", names(A))]
B

A$blogspot_grep <- grepl("blogspot", A$blog)
A$wordpress_grep <- grepl("wordpress", A$blog)
A$typepad_grep <- grepl("typepad", A$blog)
A$newsvine_grep <- grepl("newsvine", A$blog)
A$livejournal_grep <- grepl("livejournal", A$blog)



C <- A[,grep("grep", names(A))]
rowSums(C)
table( rowSums(C) )
