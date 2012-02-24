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

