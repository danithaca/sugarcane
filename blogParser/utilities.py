import glob
import re
import subprocess
import random
import sys
import os

import lxml.etree as etree
from lxml.html.clean import Cleaner

html_parser = etree.HTMLParser(remove_blank_text=True)
html_cleaner = Cleaner( style=True, scripts=True, comments=True, safe_attrs_only=True )

### Field scraper functions ####################################################

def generic_field_scraper(field_name, html_tree, file_name, xpath, cleaner):
    success = False
    xpath_count = None
    result_text = None

    try:
        xml = etree.Element( field_name )
        xpath_matches = html_tree.xpath(xpath)

        xpath_count = len(xpath_matches)
        if xpath_count > 0:
            x = xpath_matches[0]
            result_text = cleaner(x)
            xml.text = result_text
            success = True

    except Exception, err:
#        if verbose:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]      
            print(exc_type, fname, exc_tb.tb_lineno)                
    """
    except Exception as e:
        print type(e)
        print e.args
        print e

    except Exception as err:
        raise err
    """
    
    result = {
        'success' : success,
        'message' : None,
        'contents' : result_text,
        'details' : {
            'xpath_count' : xpath_count,
            }
        }

    return (result, xml)

def multiple_field_scraper(field_name, html_tree, file_name, xpath, cleaner, join_str=', '):
    success = False
    xpath_count = None
    result_text = None

    try:
        xml = etree.Element( field_name )
        xpath_matches = html_tree.xpath(xpath)

        xpath_count = len(xpath_matches)
        result_text = []
        for x in xpath_matches:
            result_text.append( cleaner(x) )
        
        xml.text = join_str.join(result_text)
        success = True

    except Exception, err:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]      
        print(exc_type, fname, exc_tb.tb_lineno)                
    
    result = {
        'success' : success,
        'message' : None,
        'contents' : result_text,
        'details' : {
            'xpath_count' : xpath_count,
            }
        }

    return (result, xml)

def empty_field_scraper(field_name, html_tree, file_name):
    result = {
        'success' : False,
        'message' : "Field scraper not declared",
        'contents' : None,
        }

    return (result, etree.Element( field_name ))


### "Cleaner" functions ########################################################
# Input: an etree xml node
# Output: cleaned text

def getNodeText( x ):
    return x.text.strip()

def cleanAndTextify( x ):
    x = html_cleaner.clean_html( x )    #Remove scripts, styles, etc.
    return etree.tostring( x, pretty_print=True )

def stripAllTags( x ):
    x = html_cleaner.clean_html( x )    #Remove scripts, styles, etc.
    t = etree.tostring( x, pretty_print=True )
    t = re.sub('<.*?>', '', t )    #Remove html tags
    t = re.sub('\s+', ' ', t )    #Remove whitespace
    return t.strip()


### External functions ########################################################
def firefox( filename ):
    subprocess.Popen(['firefox',filename])

def openBlogPostInFirefox( filepath, parser, index=None ):
    posts = parser.mapPostFiles(filepath)
    if not index: post = random.choice(posts)
    else: post = posts[index]

    firefox( post )
    return post


### Misc functions ########################################################
def filterByRegex( F, regex ):
    return [f for f in F if re.search(regex, f )]

def countXpathMatches( f, xpath ):
    H = etree.parse( f, html_parser )
    return len( H.xpath( xpath ) )

#def getFilesByRegexSearch( path, regex ):
#    return [f for f in glob.glob( path+'*' ) if re.search(regex, f )]

