from copy import deepcopy
from . import *

@profiledParser
class BlogspotParserA( BlogParser ):
        
    def extractLabels(x):
        L = x.xpath('.//a')

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
                'xpath' : "//h2[@class='date-header']",
                'cleaner' : utilities.stripAllTags,
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
