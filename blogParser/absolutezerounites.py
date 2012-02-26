from . import *

def extract_blogspot_labels(x):
    L = x.xpath('.//a')

    labels = []
    for l in L:
        if l.text: labels.append(l.text)
    return ",".join(labels)
    
def extract_comment_count(x):
    return re.findall( '\d+', x.text.strip() )[0]

@profiledParser
class AbsoluteZeroUnitesParser( BlogParser ):

    map_glob = '/[0-9]*/[0-9]*/*.html'

    field_scrapers = {
        "title"   : {
            'function' : utilities.generic_field_scraper,
            'args' : {
                'xpath' : "//h3[contains(@class,'post-title')]",
                'cleaner' : utilities.stripAllTags,#utilities.getNodeText,
                }
            },

        "author"   : {
            'function' : utilities.generic_field_scraper,
            'args' : {
                'xpath' : "//span[contains(@class,'post-author')]",#/span",
                'cleaner' : utilities.stripAllTags,
                }
            },

        "date"   : {
            'function' : utilities.generic_field_scraper,
            'args' : {
                'xpath' : "//h2[@class='date-header']/span",
                'cleaner' : utilities.getNodeText,
                }
            },

        "content"   : {
            'function' : utilities.generic_field_scraper,
            'args' : {
                'xpath' : "//div[contains(@class,'post-body')]",
                'cleaner' : utilities.cleanAndTextify,
                }
            },

        "labels"   : {
            'function' : utilities.generic_field_scraper,
            'args' : {
                'xpath' : "//span[@class='post-labels']",
                'cleaner' : extract_blogspot_labels,
                }
            },

        "comment-count"   : {
            'function' : utilities.generic_field_scraper,
            'args' : {
                'xpath' : "//div[@id='comments']/h4",
                'cleaner' : extract_comment_count,
                }
            },
        }

"""    def getLabelsFromEntryUtility(x):
        y = [utilities.getNodeText(x) for x in x.xpath('a[@rel="tag"]')]
        return ",".join( y )

    def extractCommentCount(x):
        x = x.xpath("//h3[@id='comments-title']")
        if len(x) == 0:
            return "0"
        
        c = x[0].text.split(' ')[0]
        if c == 'One':
            return "1"
        else:
            return c
    
    def getDateFromUrl(x):
        return '/'.join(x.attrib["content"].split('/')[3:6])

    def cleanAndTextify(x):
        x = deepcopy(x)
    
        removed_elements = [
            ".//div[contains(@class,'wpcom_below_post')]",
            ".//div[contains(@class,'sharedaddy')]",
            "id('wpl-likebox')",
            "id('wpcom_below_post')",
            ".//p[@class='clear']",
            ".//p[contains(@class,'postmetadata')]",
            ".//div[contains(@class,'wpadvert')]",
        ]

        for r in removed_elements:
            for e in x.xpath(r):
#                print etree.tostring(e, pretty_print=True)
                e.getparent().remove(e)
            
        return utilities.cleanAndTextify(x)
"""
