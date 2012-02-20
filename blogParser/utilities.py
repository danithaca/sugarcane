import glob, re, subprocess, random
import lxml.etree as etree
from lxml.html.clean import Cleaner

html_parser = etree.HTMLParser()
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





if __name__ == "__main__":
    """
    from parsers import BlogspotParserA
    bspa = BlogspotParserA()
    B = [
        "/scratch/unmirrored1/agong/blog_crawl_2012_01/mirrors/forumforforeignaffairs.blogspot.com/",
        "/scratch/unmirrored1/agong/blog_crawl_2012_01/mirrors/canadianinternationalpeaceproject.blogspot.com/",
        "/scratch/unmirrored1/agong/blog_crawl_2012_01/mirrors/hellishtruth.blogspot.com/",
        "/scratch/unmirrored1/agong/blog_crawl_2012_01/mirrors/femikneesm.blogspot.com/",
        "/scratch/unmirrored1/agong/blog_crawl_2012_01/mirrors/harryschwartz.blogspot.com/",
    ]

    for b in B:
        print '='*80
        print 'b'
        P = bspa.mapPostFiles(b)
        for p in P:
            r = bspa.checkPost( file(p,'r').read() )
            print r
            if not r["author"][0]:
                firefox( p )
#                p = openPostInFirefox( b, bspa, p )
                break

    for f in bspa.fields:
        print f, '\t', bspa.fields[f]

    """    

    from parsers import BlogspotParserA
#    filepath = '/scratch/unmirrored5/agong/blog_crawl_2012_01/mirrors/gdcritter.blogspot.com/'
    filepath = '/scratch/unmirrored1/agong/blog_crawl_2012_01/mirrors/tomnelson.blogspot.com/'
    parser = BlogspotParserA()
    X = parser.parseBlog( filepath, True, max_posts=20 )
    file( '/users/agong/Desktop/temp.xml', 'w' ).write( etree.tostring( X, pretty_print=True ) )
