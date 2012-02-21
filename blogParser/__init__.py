import datetime, glob, re, sys, os, random
from copy import deepcopy
import lxml.etree as etree
from lxml import html

import utilities

parser_registry = {}

def profiledParser( parser ):
    parser_registry[parser.__name__] = parser
    return parser


xml_parser = etree.XMLParser(remove_blank_text=True)

field_keys = ["title","author","date","content","labels","comment-count"]

class BlogParser(object):
    map_glob = ''       #A glob string for files to be matched
    map_except = None   #A regex string for filenames to be excluded
    map_include = None  #A regex string for filenames to be kept.
                        #If specified, this overrides map_except

    optional_fields = [] #Fields that can be omitted without throwing an error
    fields = {}         #xpath expressions that match key fields
    cleaners = {}       #functions to clean the results of xpath searches on fields

    def parseBlog(self, filepath, verbose=False, max_posts=None, filename=None):
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
            
        if filename:
            file(filename,'w').write( etree.tostring(blog_xml, pretty_print=True) )
            
        return blog_xml

    def mapPostFiles(self, filepath, verbose=False):
        if verbose: print '\tMapping post pages...'

        F = glob.glob( filepath+self.map_glob )
        
#        print '\t', len(F), filepath+self.map_glob
        if self.map_include:
            F = [ f for f in F
                        if re.search( self.map_include, f )
                ]
        elif self.map_except:
            F = [ f for f in F
                        if not re.search( self.map_include, f )
                ]
#        print len(F)

        if verbose: print '\t\tFound', len(F), 'posts.'
        return F

    def setBlogVariables( self, blog_xml, verbose=False ):
        #blog_xml.set( "blog_name", url )
        blog_xml.set( "parser", str(self.__class__.__name__))
        blog_xml.set( "parse_date", str(datetime.datetime.now()) )

    def parsePost(self, text, verbose=False, check_only=False):
        """Parse a post and return an xml entry OR result triple
        
        Arguments:
        text -- the text of the blog post
        verbose -- turns on detailed reporting for parsing and error handling
        check_only -- If this is true, parsePost returns an result triple instead of xml
        
        Returns:
        An xml object containing one entry for each field in field_keys with a corresponding
        
            OR
        
        A result object containing a dictionary of tuples in this format
            "field _name" : (   xpath_count -- int: the number of matches on the xpath query,
                                clean_success -- boolean: whether the cleaner executed successfully,
                                result_text -- text from a successful clean,
                            )
                            
        NB: A successful parser will always return one of two things in each field:
            (1, True, "some string...") -- A match on a unique field, OR
            (0, True, None)             -- An optional field
        """
        
        post_xml = etree.Element( "post" )
        H = html.fromstring(text)

        result = {}
        for f in field_keys:
            try:
                xpath_count = None
                clean_success = None
                result_text = None
                
                if f in self.fields:
                    e = etree.SubElement( post_xml, f )
                    X = H.xpath(self.fields[f])
                    xpath_count = len(X)
                    
                    clean_success = False
                    if xpath_count > 0:
                        x = X[0]
                        if f in self.cleaners:
                            e.text = self.cleaners[f]( x )
                        else:
                            e.text = etree.tostring( x )
                        result_text = e.text
                        clean_success = True
                        
                    elif f in self.optional_fields:
                        clean_success = True

                elif f in self.optional_fields:
                    xpath_count = 0
                    clean_success = True

            except Exception, err:
                if verbose:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]      
                    print(exc_type, fname, exc_tb.tb_lineno)                

#            except Exception as e:
#                print type(e)
#                print e.args
#                print e

#            except Exception as err:
#                raise err

            result[f] = ( xpath_count, clean_success, result_text )

        if check_only:
            return result
        else:
            return post_xml

    def convertToHtml(self, blog_xml, filename=None):
        blog_html = etree.Element('html')

        head_html = etree.SubElement( blog_html, 'head' )
        head_html.append( etree.Element("link", REL="StyleSheet", HREF="article_style.css", TYPE="text/css") )
        e = etree.Element( "meta", content="text/html; charset=UTF-8" )
        e.set("http-equiv", "Content-Type")
        head_html.append(e)

        body_html = etree.Element('body')
        for x in blog_xml.xpath('//post'):
            body_html.append( self.convertPostToHtml(x) )
        blog_html.append(body_html)

        if filename:
            file(filename,'w').write( etree.tostring(blog_html, pretty_print=True) )

        return blog_html

    def convertPostToHtml(self, post_xml):
        doc_div = etree.Element("div")
        doc_div.set("class", "document")

        #Create the doc-header div, with all sub-divs
        doc_header = etree.Element("div")
        doc_header.set("class", "document-header")
        for f in ["title","author","date","labels","comment-count"]:
            try:
                e = etree.Element("div")
                e.set("class", f)
                e.text = post_xml.xpath(f)[0].text
                if e.text == None:
                    e.text = "&nbsp;"
                doc_header.append(e)
            except IndexError:
                pass
        doc_div.append(doc_header)
        
        doc_content = etree.Element("div")
        doc_content.set("class", "document-content")

        S = post_xml.xpath('content')
        s = S[0].text
        f = etree.fromstring(s, xml_parser)
        if f is None:
            doc_content.text = "&nbsp;"
        else:
            doc_content.append(f)
        

        doc_div.append(doc_content)

        return doc_div


"""Import the actual parsers..."""
from blogspot_a import *  
from wordpress_a import *  
from wordpress_b import *  
from typepad_a import *  
from newsvine_a import *  
from livejournal_a import *  



