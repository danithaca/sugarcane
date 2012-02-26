from . import *

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
                'cleaner' : utilities.cleanAndTextify,
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
            'function' : utilities.empty_field_scraper,
            'args' : {}
            },

        "comment-count"   : {
            'function' : utilities.empty_field_scraper,
            'args' : {}
            }
        }

