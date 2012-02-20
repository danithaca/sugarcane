setwd("/home/agong/Dropbox/projects/active/blog_parsers/mturk_post_counting_task")

A <- read.csv("Batch_708085_batch_results.csv")

A$AcceptTime
A$AssignmentDurationInSeconds

wts <- A$WorkTimeInSeconds 
plot( wts )
plot( density( wts, 3 ))
M <- lm( wts>60 ~ c(1:109) )
summary(M)

strptime( A$AcceptTime, )

/home/agong/Dropbox/projects/active/blog_parsers/mturk_post_counting_task
