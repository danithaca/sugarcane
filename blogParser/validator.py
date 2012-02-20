parser_registry = {}

def validatedParser( parser ):
    parser_registry[parser.__name__] = parser
    return parser




#Use a mix of human and computer validation techniques


def checkFields(parser, xml):
    if xml is not None:
        #Return matches by field
        return [len(xml.xpath('//'+f)) for f in parser.fields_xpath]
        
    else:
        #Return header
        return [ f for f in parser.fields_xpath ]