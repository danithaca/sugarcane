from django.conf.urls.defaults import patterns, include, url
from django.utils import simplejson

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sugarcane.views.home', name='home'),
    url(r'^sugarcane/', 'sugarcane.urls.check_bapf'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

########################################################################

import random
from django.http import HttpResponse

from blogParser.parsers import parser_registry, field_keys

def checkBlogAgainstParser( blog, parser, k=20 ):
    P = parser.mapPostFiles(blog)
    random.shuffle(P)
    
    #Set up an empty results object
    results = {}
    for f in field_keys:
        results[f] = {"xpath":0,"cleaner":0}
    
    #Take up to the first k posts of the blog
    for p in P[:k]:
        #Check fields against the parser
        result = parser.checkPost(file(p,'r').read())
        
        #Compile results
        for f in result:
            if result[f][0]: results[f]["xpath"] += 1
            if result[f][1]: results[f]["cleaner"] += 1

    #Store to csv
    return results

def check_bapf( request ):
    r = checkBlogAgainstParser( request.GET["blog"], parser_registry[request.GET["parser"]]() )#, k=5 )
    print r
    return HttpResponse(simplejson.dumps(r, indent=2), mimetype = 'application/javascript')

#for p in parser_registry:
#    print parser_registry[p]()
#   print p
#   print '^sugarcane/'+p




#http://localhost:8000/sugarcane/BlogspotParserA?/scratch/unmirrored1/agong/blog_crawl_2012_01/mirrors/boogeymanchronicles.blogspot.com/
#http://localhost:8000/sugarcane/BlogspotParserA?filename=/scratch/unmirrored1/agong/blog_crawl_2012_01/mirrors/boogeymanchronicles.blogspot.com/
#http://localhost:8000/sugarcane/?parser=BlogspotParserA&blog=/scratch/unmirrored1/agong/blog_crawl_2012_01/mirrors/boogeymanchronicles.blogspot.com/
#http://localhost:8000/sugarcane/?parser=BlogspotParserA&blog=/scratch/unmirrored1/agong/blog_crawl_2012_01/mirrors/boogeymanchronicles.blogspot.com/&field=author
