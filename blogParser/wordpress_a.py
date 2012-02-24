from . import *

@profiledParser
class WordpressParserA( BlogParser ):

    def get_labels_from_entry_utility(x):
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

    map_glob = '/[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]/*/index.html'

    field_scrapers = {
        "title"   : {
            'function' : utilities.generic_field_scraper,
            'args' : {
                'xpath' : "//h1[@class='entry-title']",
                'cleaner' : utilities.getNodeText,
                }
            },

        "author"   : {
            'function' : utilities.generic_field_scraper,
            'args' : {
                'xpath' : "//span[@class='author vcard']",
                'cleaner' : utilities.stripAllTags,
                }
            },

        "date"   : {
            'function' : utilities.generic_field_scraper,
            'args' : {
                'xpath' : "//span[@class='entry-date']",
                'cleaner' : utilities.getNodeText,
                }
            },

        "content"   : {
            'function' : utilities.generic_field_scraper,
            'args' : {
                'xpath' : "//div[@class='entry-content']",
                'cleaner' : utilities.cleanAndTextify,
                }
            },

        "labels"   : {
            'function' : utilities.generic_field_scraper,
            'args' : {
                'xpath' : "//div[@class='entry-utility']",
                'cleaner' : get_labels_from_entry_utility,
                }
            },

        "comment-count"   : {
            'function' : utilities.generic_field_scraper,
            'args' : {
                'xpath' : "//div[@id='comments']",
                'cleaner' : extractCommentCount,
                }
            },
        }



"""
@profiledParser
class WordpressParserA( BlogParser ):

    def get_labels_from_entry_utility(x):
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

    map_glob = '/[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]/*/index.html'
    
    fields = {
        "title"   : "//h1[@class='entry-title']",
        "author"  : "//span[@class='author vcard']",
        "date"    : "//span[@class='entry-date']",
        "content" : "//div[@class='entry-content']",
        "labels"  : "//div[@class='entry-utility']",
#        "labels"  : "//div[@class='entry-info']",
        "comment-count" : "//div[@id='comments']",
    }

    cleaners = {
        "title"   : utilities.getNodeText,
        "author"  : utilities.stripAllTags,
        "date"    : utilities.getNodeText,
        "content" : utilities.cleanAndTextify,
        "labels"  : get_labels_from_entry_utility,
        "comment-count" : extractCommentCount,
    }
"""
