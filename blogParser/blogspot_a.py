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

    fields = {
        "title"   : "//h3[@class='post-title entry-title']",
#        "author"  : "//span[@class='post-author vcard']/span/a",
        "author"  : "//span[@class='post-author vcard']/span",
        "date"    : "//h2[@class='date-header']/span",
        "content" : "//div[@class='post-body entry-content']",
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

