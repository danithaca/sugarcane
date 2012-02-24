from . import *

@profiledParser
class WordpressParserB( BlogParser ):

    def getLabelsFromEntryUtility(x):
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


    map_glob = '/[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]/*/index.html'

    field_scrapers = {
        "title"   : {
            'function' : utilities.generic_field_scraper,
            'args' : {
                'xpath' : "//div[contains(@class,'post')]/h2",
                'cleaner' : utilities.getNodeText,
                }
            },

        "author"   : {
            'function' : utilities.empty_field_scraper,
            'args' : {}
            },

        "date"   : {
            'function' : utilities.generic_field_scraper,
            'args' : {
                'xpath' : "//meta[@property='og:url']",
                'cleaner' : getDateFromUrl,
                }
            },

        "content"   : {
            'function' : utilities.generic_field_scraper,
            'args' : {
                'xpath' : "//div[@class='entry']",
                'cleaner' : cleanAndTextify,
                }
            },

        "labels"   : {
            'function' : utilities.generic_field_scraper,
            'args' : {
                'xpath' : "//p[@class='clear']",
                'cleaner' : getLabelsFromEntryUtility,
                }
            },

        "comment-count"   : {
            'function' : utilities.empty_field_scraper,
            'args' : {}
            }
        }
"""
    optional_fields = ['labels']
    
    fields = {
        "title"   : "//div[contains(@class,'post')]/h2",
#        "author"  : "//span[@class='author vcard']",
        "date"    : "//meta[@property='og:url']",
        "content" : "//div[@class='entry']",
        "labels"  : "//p[@class='clear']",
#        "comment-count" : "//div[@id='comments']",
    }

    cleaners = {
        "title"   : utilities.getNodeText,
#        "author"  : lambda:"",
        "date"    : getDateFromUrl,
        "content" : cleanAndTextify,#utilities.cleanAndTextify,
        "labels"  : getLabelsFromEntryUtility,
#        "comment-count" : extractCommentCount,
    }

"""
