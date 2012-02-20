#Load and inspect the data

    #(will need to increment the counter on "test")
    A <- read.csv("map-test-2.csv")

    head(A)
    names(A)
    dim(A)

#Check url names for major blog hosting brands
    A$blogspot_grep <- grepl("blogspot", A$blog)
    A$wordpress_grep <- grepl("wordpress", A$blog)
    A$typepad_grep <- grepl("typepad", A$blog)
    A$newsvine_grep <- grepl("newsvine", A$blog)
    A$livejournal_grep <- grepl("livejournal", A$blog)

#Create a dataframe of only the parser results
    B <- A[,grep("Parser", names(A))]
    names(B)

    B1 <- log(B+1)
    B2 <- B>0
    names(B1) <- c("wp_count","lj_count","bs_count","nv_count","tp_count")
    colnames(B2) <- c("wp_any","lj_any","bs_any","nv_any","tp_any")


#Create a dataframe of grep results
    C <- A[,grep("grep", names(A))]
    rowSums(C)
    table( rowSums(C) )

    #This is good: 111 match exactly once, and none match more than once.
    #Only 62 don't match at all.

#Classify based on name
    url_class <- as.matrix(C) %*% as.matrix(c(1:5))
    url_class[url_class==0] <- NA
    table(url_class)

#Create a variable identifying the grep class
    class <- as.matrix(C) %*% as.matrix(c(1:5))
    class[class==0] <- NA

#Create a combined data frame
    D <- cbind(B1,B2,url_class)

#Test models
#    mlogit( url_class ~ 1|WordpressParserA + BlogspotParserA + NewsvineParserA + TypepadParserA +, data=D, varying=NULL )
#    mlogit( url_class ~ 1|wp_any+lj_any+bs_any+nv_any+tp_any+wp_any+lj_any+bs_any+nv_any+tp_any, data=D, varying=NULL )
#    M <- mlogit( url_class ~ 1|wp_count+bs_count+nv_count+tp_count+wp_any+bs_any+nv_any+tp_any, data=D, varying=NULL )
    M <- mlogit( url_class ~ 1|wp_count+bs_count+nv_count+tp_count, data=D, varying=NULL )
    summary(M)


    M <- glm( I(url_class==1) ~ wp_count+bs_count+nv_count+tp_count, data=D )
    M <- glm( I(url_class==2) ~ wp_count+bs_count+nv_count+tp_count, data=D )
    M <- glm( I(url_class==3) ~ wp_count+bs_count+nv_count+tp_count, data=D )
    M <- glm( I(url_class==4) ~ wp_count+bs_count+nv_count+tp_count, data=D )

    M <- glm( I(url_class==1) ~ wp_count+bs_count+nv_count+tp_count+wp_any+bs_any+nv_any+tp_any, data=D )
    
#Store results
#    write.csv(A, "cum_map_test.csv")

    
    setwd("~/Dropbox/projects/active/blog_parsers/")
    A <- read.csv("results/cum_map_test.csv")

    names(A)
    dim(A)

    hist( log(A$file_count) )

    plot( density( log(A$file_count), na.rm=T, .5, from=0))
    abline( v=log(20))
    
    table(A$file_count<20)
    
    table(A$url_matches, A$very_few_files)
    
    B <- A[!A$very_few_files,]
    dim(B)
    
    table(B$url_matches)
    