from blogParser import parser_registry
import blogParser.utilities as utilities

content_scrapers = [
    {
        'function' : utilities.generic_field_scraper,
        'args' : {
            'xpath' : "//h3[contains(@class,'post-title')]",
            'cleaner' : utilities.stripAllTags,#utilities.getNodeText,
            }
    },
]

for p in parser_registry:
    P = parser_registry[p]()
    if "content" in P.field_scrapers:
        content_scrapers += P.field_scrapers["content"]
#    print scraper
#    content_scrapers += 
