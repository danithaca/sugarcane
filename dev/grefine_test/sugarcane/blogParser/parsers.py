import datetime, glob, re, sys, os, random
import lxml.etree as etree
from lxml import html
#from lxml.html.clean import Cleaner

import utilities
#from profiler import profiledParser, parser_registry

parser_registry = {}

def profiledParser( parser ):
    parser_registry[parser.__name__] = parser
    return parser


html_parser = etree.HTMLParser()

field_keys = ["title","author","date","content","labels","comment-count"]

class BlogParser(object):
    fields = {}     #xpath expressions that match key fields
    cleaners = {}   #functions to clean the results of xpath searches on fields

    def parseBlog(self, filepath, verbose=False, max_posts=None):
        if verbose: print 'Parsing blog at filepath', filepath
        blog_xml = etree.Element( "blog" )

        #self.setExpressions( url )
        self.setBlogVariables( blog_xml, verbose )
        
        post_files = self.mapPostFiles(filepath, verbose)
        if max_posts:
            random.shuffle( post_files )
            post_files = post_files[:max_posts]

        for p in post_files:
            if verbose: print '\tParsing post in file', p
            post_xml = self.parsePost( file(p, 'r').read(), verbose )
            blog_xml.append( post_xml )
            
        return blog_xml

    def mapPostFiles(self, filepath, verbose=False): pass
    def setBlogVariables( self, blog_xml, verbose=False ):
        #blog_xml.set( "blog_name", url )
        blog_xml.set( "parser", str(self.__class__.__name__))
        blog_xml.set( "parse_date", str(datetime.datetime.now()) )

    def checkPost(self, text, verbose=False):
        post_xml = etree.Element( "post" )
        H = html.fromstring(text)

        result = {}
        for f in field_keys:
            xpath_count, clean_success = None, None
            try:
                if f in self.fields:
                    e = etree.SubElement( post_xml, f )
                    X = H.xpath(self.fields[f])
                    xpath_count = len(X)
                    
                    if len(X) > 0:
                        clean_success = False
                        x = X[0]
                        if f in self.cleaners:
                            e.text = self.cleaners[f]( x )
                        else:
                            e.text = etree.tostring( x )
                        clean_success = True

            #From: http://stackoverflow.com/questions/1278705/python-when-i-catch-an-exception-how-do-i-get-the-type-file-and-line-number
            except Exception, e:
                if verbose:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]      
                    print(exc_type, fname, exc_tb.tb_lineno)                

#            except Exception as e:
#                print type(e)
#                print e.args
#                print e

#            except Exception as e:
#                raise e

            result[f] = ( xpath_count, clean_success )

        return result
    
    
    def parsePost(self, text, verbose=False):
        post_xml = etree.Element( "post" )
        H = html.fromstring(text)
        for f in field_keys:
            if f in self.fields:
                e = etree.SubElement( post_xml, f )
                try:
                    x = H.xpath(self.fields[f])[0]
                    if f in self.cleaners:
                        e.text = self.cleaners[f]( x )
                    else:
                        e.text = etree.tostring( x )
                except:
                    if verbose: print '\t\tError in field', f
                    post_xml.set("parse_error", "True")
                    pass

        return post_xml

@profiledParser
class BlogspotParserA( BlogParser ):

    def mapPostFiles(self, filepath, verbose=False):
        if verbose: print '\tMapping post pages...'
        F = glob.glob( filepath+'/[0-9]*/[0-9]*/*.html' )
        if verbose: print '\t\tFound', len(F), 'posts.'
        return F
        
    def extractLabels(x):
        L = x.xpath('.//a')
#        if not L: return ""

        labels = []
        for l in L:
            if l.text: labels.append(l.text)
        return ",".join(labels)
                    
    def extractCommentCount(x):
        return re.findall( '\d+', x.text.strip() )[0]

    fields = {
        "title"   : "//h3[@class='post-title entry-title']",
#        "author"  : "//span[@class='post-author vcard']/span/a",
        "author"  : "//span[@class='post-author vcard']/span",
        "date"    : "//h2[@class='date-header']/span",
        "content" : "//div[@class='post-body entry-content']",
        "labels"  : "//span[@class='post-labels']",
        "comment-count" : "//div[@id='comments']/h4",
    }

    cleaners = {
        "title"   : utilities.getNodeText,
#        "author"  : utilities.getNodeText,
        "author"  : utilities.stripAllTags,
        "date"    : utilities.getNodeText,
        "content" : utilities.cleanAndTextify,
        "labels"  : extractLabels,
        "comment-count" : extractCommentCount,
    }

"""
if __name__ == "__main__":
    filepath = '/scratch/unmirrored5/agong/blog_crawl_2012_01/mirrors/gdcritter.blogspot.com/'
    parser = BlogspotParserA()
    X = parser.parseBlog( filepath, False )
#    file( '/users/agong/Desktop/temp.xml', 'w' ).write( etree.tostring( X, pretty_print=True ) )
"""
