	A <- read.csv("blogParsingResults.csv")
#	dim(A)
#	names(A)

	C <- reshape(A, idvar="blog_url", timevar="blog_type", direction="wide" )
#	dim(C)
#	names(C)

#How many total blogs were profiled?
	print( "Total blogs" )
	print( length(C$blog_url) )

	grep( "total_files", names(C) )
	x <- C[,grep( "total_files", names(C) )]

#How many blogs had at least one file match?
	print( "Blogs with at least one matching file" )
	C$blog_url[rowSums(x)>0]
	sum(rowSums(x)>0, na.rm=TRUE)

#How many blogs didn't have any file matches?
	print( "Blogs with no matching files" )
	C$blog_url[!rowSums(x)>0]
	sum(!rowSums(x)>0, na.rm=TRUE)

#How many blogs matched files on more than one type?
	print( "Blogs with multiple types matching files" )
	C$blog_url[rowSums(x>0)>1]
	sum(rowSums(x>0)>1, na.rm=TRUE)




#Which blog-type pairs had file matches but less than perfect content acquisition?
	v <- (A$total_files>0) & (A$has_content<1)
	paste( A$blog_url, A$blog_type, sep=" ")[v]

#Which blog-type pairs have perfect content acquisition?
	v <- (A$total_files>0) & (A$has_content==1)
	paste( A$blog_url, A$blog_type, sep=" ")[v]
	sum( v, na.rm=TRUE )

	print( "Percent with content acquisition" )
	(sum( v, na.rm=TRUE ) - sum(duplicated(A$blog_url[v]))) /length(C$blog_url)
	#Note: the "duplicated" bit is to make sure that blogs with perfect content matching on more than one type will not throw off the percentage.  This is unlikely, but possible.

#Which blog-type pairs have perfect date acquisition?
#Which blog-type pairs have perfect title acquisition?
#Which blog-type pairs have perfect lables acquisition?
#Which blog-type pairs have perfect comments acquisition?





#Timing
#This doesn't work...
	T <- as.numeric(strsplit( as.character(A$file_match_time_elapsed), "[:]" ))
	T <- as.matrix( strsplit( as.character(A$file_match_time_elapsed), "[:]" ) )
	T
	T2 <- as.numeric(T[1])*3600  + as.numeric(T[2])*60 + as.numeric(T[3])
	T2 <- as.numeric(T[1,])*3600  + as.numeric(T[2,])*60 + as.numeric(T[3,])

	strptime( 
	strptime( as.character(A$file_match_time_elapsed) )
	strptime( as.character(A$file_match_time_elapsed), "%T" )
	plot( density( strptime( as.character(A$file_match_time_elapsed), "%T" ) ) )
	plot( density( strptime( as.character(A$file_match_time_elapsed), "%T" ) ) )
	strptime( as.character(A$file_match_time_elapsed), "%T" )


