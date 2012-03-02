from copy import deepcopy
from . import *

def get_date_from_wordpress_meta_tag(x):
    return '/'.join(x.attrib["content"].split('/')[3:6])

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




@profiledParser
class WordpressParserC( BlogParser ):

    def get_date_from_wordpress_meta_tag(x):
        return '/'.join(x.attrib["content"].split('/')[3:6])

    map_glob = '/[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]/*/index.html'

    field_scrapers = {
        "title"   : {
            'function' : utilities.generic_field_scraper,
            'args' : {
                'xpath' : "//h2[contains(@class,'post-titulo')]",
                'cleaner' : utilities.stripAllTags,
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
                'cleaner' : get_date_from_wordpress_meta_tag,
                }
            },

        "content"   : {
            'function' : utilities.generic_field_scraper,
            'args' : {
                'xpath' : "//div[@class='postentry']",
                'cleaner' : utilities.cleanAndTextify,
                }
            },

        "labels"   : {
            'function' : utilities.multiple_field_scraper,
            'args' : {
                'xpath' : "//a[contains(@rel,'tag')]",
                'cleaner' : utilities.stripAllTags,
                }
            },

        "comment-count"   : {
            'function' : utilities.empty_field_scraper,
            'args' : {}
            }
        }


@profiledParser
class WordpressParserD( WordpressParserA ):

    def matchClassAndCleanElement( field_name, html_tree, xpath, class_name, cleaner ):
        success = False
        xpath_count = None
        result_text = None

        try:
            xml = etree.Element( field_name )
            xpath_matches = html_tree.xpath(xpath)

            xpath_count = 0
            class_matches = []
            print len(xpath_matches)
            for x in xpath_matches:
                print x
                if 'class' in x.attrib:
                    class_tags = x.attrib["class"].split(' ')
                    if class_name in class_tags:
                        xpath_count += 1
                        class_matches.append(x)

            if xpath_count > 0:
                x = class_matches[0]
                result_text = cleaner(x)
                xml.text = result_text
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

    field_scrapers = deepcopy(WordpressParserA.field_scrapers)
    """
    field_scrapers["content"] = {
        'function' : matchClassAndCleanElement,
        'args' : {
            'xpath' : "//div[contains(@class,'post')]",
            'class_name' : "post",
            'cleaner' : utilities.cleanAndTextify,
            }
        }
    """
    
    field_scrapers["content"] = {
        'function' : utilities.generic_field_scraper,
        'args' : {
            'xpath' : "//div[contains(@class,'entry-content')]",
            'cleaner' : utilities.cleanAndTextify,
            }
        }

    field_scrapers["labels"] = {
        'function' : utilities.multiple_field_scraper,
        'args' : {
            'xpath' : "//a[contains(@rel,'tag')]",
            'cleaner' : utilities.stripAllTags,
            }
        }

    field_scrapers["date"] = {
        'function' : utilities.generic_field_scraper,
        'args' : {
            'xpath' : "//abbr[@class='published']/@title",
            'cleaner' : lambda x: x#get_date_from_wordpress_meta_tag,
            }
        }

@profiledParser
class WordpressParserE( WordpressParserC ):
