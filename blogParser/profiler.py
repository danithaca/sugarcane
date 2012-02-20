parser_registry = {}

def profiledParser( parser ):
    parser_registry[parser.__name__] = parser
    return parser

#def getParserRegistry():
#    return parser_registry
