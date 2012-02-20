import random

import parsers, utilities


def checkBlogAgainstParser( blog, parser, k=20 ):
#    start_time = datetime.datetime.now()
    P = parser.mapPostFiles(blog)
    random.shuffle(P)
    
    #Set up an empty results object
    results = {}
    for f in parsers.field_keys: results[f] = [0,0]
    
    #Take up to the first k posts of the blog
    for p in P[:k]:
        #Check fields against the parser
        result = parser.checkPost(file(p,'r').read())
        
        #Compile results
        for f in result:
            if result[f][0] == 1: results[f][0] += 1
            if result[f][1]: results[f][1] += 1

    #Store to csv
    return results
