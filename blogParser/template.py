from . import *

@profiledParser
class TemplateParser(Parser):

    field_scrapers = {
        "title"   : {
            'function' : utilities.empty_field_scraper,
            'args' : {}
            },

        "author"   : {
            'function' : utilities.empty_field_scraper,
            'args' : {}
            },

        "date"   : {
            'function' : utilities.empty_field_scraper,
            'args' : {}
            },

        "content"   : {
            'function' : utilities.empty_field_scraper,
            'args' : {}
            },

        "labels"   : {
            'function' : utilities.empty_field_scraper,
            'args' : {}
            },

#        "labels"   : {
#            'function' : utilities.generic_field_scraper,
#            'args' : {
#                'xpath' : "//p[@class='clear']",
#                'cleaner' : getLabelsFromEntryUtility,
#                }
#            },

        "comment-count"   : {
            'function' : utilities.empty_field_scraper,
            'args' : {}
            }
        }
