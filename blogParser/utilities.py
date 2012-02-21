import glob, re, subprocess, random
import lxml.etree as etree
from lxml.html.clean import Cleaner

html_parser = etree.HTMLParser(remove_blank_text=True)
html_cleaner = Cleaner( style=True, scripts=True, comments=True, safe_attrs_only=True )

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

