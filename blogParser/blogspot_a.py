from . import *

@profiledParser
class BlogspotParserA( BlogParser ):
        
    def extractLabels(x):
        L = x.xpath('.//a')
#        if not L: return ""

        labels = []
        for l in L:
            if l.text: labels.append(l.text)
        return ",".join(labels)
                    
    def extractCommentCount(x):
        return re.findall( '\d+', x.text.strip() )[0]
        
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
                'cleaner' : extractLabels,
                }
            },

        "comment-count"   : {
            'function' : utilities.generic_field_scraper,
            'args' : {
                'xpath' : "//div[@id='comments']/h4",
                'cleaner' : extractCommentCount,
                }
            },
        }

"""

    fields = {
        "title"   : "//h3[@class='post-title entry-title']",
#        "author"  : "//span[@class='post-author vcard']/span/a",
#        "author"  : "//span[@class='post-author vcard']/span",
        "author"  : "//span[contains(@class,'post-author')]/span",
        "date"    : "//h2[@class='date-header']/span",
#        "content" : "//div[@class='post-body entry-content']",
        "content" : "//div[contains(@class,'post-body')]",
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
