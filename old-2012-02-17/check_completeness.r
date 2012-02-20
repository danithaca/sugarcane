    setwd("~/Dropbox/projects/active/blog_parsers/")
    A <- read.csv("results/check_BlogspotParserA.csv")

    names(A)
    dim(A)

#How many blogs failed to load *any* posts?
    table( A$post_count > 0 )

#hist(A$title_fields/A$post_count)

#Calculate conversion rates from posts > fields > cleaners
    A$title_field_conversion <- A$title_fields/pmin(20,A$post_count,na.rm=T)
    A$author_field_conversion <- A$author_fields/pmin(20,A$post_count,na.rm=T)
    A$date_field_conversion <- A$date_fields/pmin(20,A$post_count,na.rm=T)
    A$content_field_conversion <- A$content_fields/pmin(20,A$post_count,na.rm=T)
    A$labels_field_conversion <- A$labels_fields/pmin(20,A$post_count,na.rm=T)
    A$comment.count_field_conversion <- A$comment.count_fields/pmin(20,A$post_count,na.rm=T)
    
    A$title_cleaner_conversion <- A$title_cleaners/A$title_fields
    A$author_cleaner_conversion <- A$author_cleaners/A$author_fields
    A$date_cleaner_conversion <- A$date_cleaners/A$date_fields
    A$content_cleaner_conversion <- A$content_cleaners/A$content_fields
    A$labels_cleaner_conversion <- A$labels_cleaners/A$labels_fields
    A$comment.count_cleaner_conversion <- A$comment.count_cleaners/A$comment.count_fields

    A$title_total_conversion <- A$title_cleaners/pmin(20,A$post_count,na.rm=T)
    A$author_total_conversion <- A$author_cleaners/pmin(20,A$post_count,na.rm=T)
    A$date_total_conversion <- A$date_cleaners/pmin(20,A$post_count,na.rm=T)
    A$content_total_conversion <- A$content_cleaners/pmin(20,A$post_count,na.rm=T)
    A$labels_total_conversion <- A$labels_cleaners/pmin(20,A$post_count,na.rm=T)
    A$comment.count_total_conversion <- A$comment.count_cleaners/pmin(20,A$post_count,na.rm=T)

pdf( "results/conversion_BlogSpotParserA.pdf" )

#Check distributions of total rates -- do we have much partial conversion?
    plot( density(A$title_total_conversion, .01, from=0, to=1, na.rm=T) )
    plot( density(A$author_total_conversion, .01, from=0, to=1, na.rm=T) )
    plot( density(A$date_total_conversion, .01, from=0, to=1, na.rm=T) )
    plot( density(A$content_total_conversion, .01, from=0, to=1, na.rm=T) )
    plot( density(A$labels_total_conversion, .01, from=0, to=1, na.rm=T) )
    plot( density(A$comment.count_total_conversion, .01, from=0, to=1, na.rm=T) )

#Show proportions of perfect conversion at each stage
    M <- cbind(
      colMeans( A[,grep("field_conversion", names(A))]==1, na.rm=T ),
      colMeans( A[,grep("cleaner_conversion", names(A))]==1, na.rm=T ),
      colMeans( A[,grep("total_conversion", names(A))]==1, na.rm=T )
    )

    rownames(M) <- c("title","author","date","content","labels")
    colnames(M) <- c("field","cleaner","total")

    dotchart(t(M), pch=c(19,17,15))
    #Looks like we're losing blogs on the fields phase -- most cleaners seem to work okay.

#Check correlations between conversion on different fields
    B <- A[,grep("total_conversion", names(A))]
    cor(B, use="pairwise.complete")
    #They seem to be highly correlated.

#Check numbers of blogs with perfect conversion in each category
    #5 means all five fields had perfect conversion
    #4 means 4 of 5 fields     "  "
    #...
    table(rowSums(B==1))
    #42 out of 72
    
    #90% conversion?
    table(rowSums(B>.9))
    #Not zero, but not many, either.
    #50 out of 72
    
    dim(B)
    dim(A)
    A$blog[rowSums(B==1, na.rm=T)==4]

dev.off()
head(A)