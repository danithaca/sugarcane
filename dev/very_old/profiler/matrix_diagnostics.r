A <- read.csv("blog_tag_matrix.csv")
dim(A)
names(A)

colSums(A[3:dim(A)[2]])


searchForSimilarities <- function( my_vector, threshold=.95, mode="correlation" ){
	if( mode=="correlation") B <- unlist(lapply( c(3:dim(A)[2]), function(x){cor( my_vector, A[,x])} ))
		# "The correlation between tag [x] and [my_vector] is at least [threshold]"

	if( mode=="recall") B <- unlist(lapply( c(3:dim(A)[2]), function(x){ sum(A[my_vector==1,x])/sum(my_vector) } ))
		#"[Threshold] percent of sites matching [my_vector] also contain tag [x]"

	if( mode=="precision") B <- unlist(lapply( c(3:dim(A)[2]), function(x){ sum(A[my_vector==1,x])/sum(A[,x]) } ))
		#"[Threshold] percent of sites with tag [x] also match [my_vector]"

	return( names(A)[c(3:dim(A)[2])][B>threshold] )
}

searchForSimilarities( grepl( 'blogspot', A$url ), .90, "recall" )
searchForSimilarities( grepl( 'wordpress', A$url ), .70, "precision" )
searchForSimilarities( A$post.body, .90 )
searchForSimilarities( A$post.body, .90 )
searchForSimilarities( A$post.body, .90, "recall" )

sum( grepl( "(blogspot)|(wordpress)|(livejournal)|(tumblr)|(newsvine)|(typepad)", A$url ) )/dim(A)[1]
#6 blog urls have 60% coverage
# There are probably some differences in format (-coverage)
# But there are certainly many other blogs that use these formats (+coverage)


#What do wordpress blogs have in common?
searchForSimilarities( grepl( 'wordpress', A$url ), .70, "precision" )
searchForSimilarities( A$post.body, .90 )
searchForSimilarities( A$post.body, .90, "recall" )
searchForSimilarities( grepl( 'wordpress', A$url ), .70, "recall" )
searchForSimilarities( grepl( 'wordpress', A$url ), .90, "recall" )
searchForSimilarities( A$content, .90, "recall" )
searchForSimilarities( A$content, .90 )
searchForSimilarities( A$content, .7 )
searchForSimilarities( A$content, .4 )
searchForSimilarities( A$content, .9, "precision" )
searchForSimilarities( A$content, .9, "precision" )
searchForSimilarities( A$content, .99, "precision" )
searchForSimilarities( A$content.box, .99, "precision" )
searchForSimilarities( A$content.box, .99 )
searchForSimilarities( A$content.box, .95 )
searchForSimilarities( A$content.container, .95 )
searchForSimilarities( A$content.container, .90 )
table( A$content.container, grepl("wordpress", A$url) )
