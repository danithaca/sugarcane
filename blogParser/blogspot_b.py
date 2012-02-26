from copy import deepcopy

from . import *
#from blogspot_a import BlogspotParserA

@profiledParser
class BlogspotParserB( BlogspotParserA ):
    field_scrapers = deepcopy(BlogspotParserA.field_scrapers)
    
    field_scrapers["date"] = {
        'function' : utilities.generic_field_scraper,
        'args' : {
            'xpath' : "//h2[@class='date-header']",
            'cleaner' : utilities.stripAllTags,
            }
        }
