import datetime
import glob
import re
import os
import random

from copy import deepcopy
import lxml.etree as etree
from lxml import html

import utilities

parser_registry = {}

def profiledParser( parser ):
    parser_registry[parser.__name__] = parser
    return parser


xml_parser = etree.XMLParser(remove_blank_text=False)

field_keys = ["title","author","date","content","labels","comment-count"]

class BlogParser(object):
    map_glob = ''       #A glob string for files to be matched
    map_except = None   #A regex string for filenames to be excluded
    map_include = None  #A regex string for filenames to be kept.
                        #If specified, this overrides map_except

#    optional_fields = [] #Fields that can be omitted without throwing an error
#    fields = {}         #xpath expressions that match key fields
#    cleaners = {}       #functions to clean the results of xpath searches on fields

    field_scrapers = {}

    def parseBlog(self, filepath, max_posts=None, shuffle=False, filename=None, verbose=False ):
        if verbose: print 'Parsing blog at filepath', filepath
                
        post_files = self.mapPostFiles(filepath, verbose)
        if shuffle:
            random.shuffle( post_files )
        if max_posts:
            post_files = post_files[:max_posts]

        results = {}
        blog_xml = etree.Element( "blog" )
        #self.setExpressions( url )
        self.setBlogVariables( blog_xml, verbose )

        for p in post_files:
            if verbose: print '\tParsing post in file', p

            try:
                (result, xml) = self.parsePost(file(p, 'r').read(), verbose)
                results[p] = result
                blog_xml.append(xml)

            #! This is a hack to capture directories parsed as files
            except IOError:
#                print 'IOError'
                pass
            
        if filename:
            file(filename,'w').write( etree.tostring(blog_xml, pretty_print=True) )
        
        return (results, blog_xml)

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

    def parsePost(self, text, verbose=False):#, check_only=False):
        """Parse a post and return a result dict and xml object"""
        
        post_xml = etree.Element( "post" )
        html_tree = html.fromstring(text)

        result = {}
        for field_name in field_keys:
            (r, x) = self.field_scrapers[field_name]["function"](
                field_name,
                html_tree,
                **self.field_scrapers[field_name]["args"])
            post_xml.append(x)
            result[field_name] = r

        return (result, post_xml)
        
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

        #Remove empty paragraphs        
        for p in f.xpath("p"):
            t = p.text
            if not (t and t.strip()):
                p.getparent().remove(p)

        #remove empty divs
        for p in f.xpath("div"):
            t = p.text
            if not (t and t.strip()):
                p.getparent().remove(p)
                
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
from wordpress_c import *
#from typepad_a import *  
#from newsvine_a import *  
#from livejournal_a import *  

from absolutezerounites import AbsoluteZeroUnitesParser

