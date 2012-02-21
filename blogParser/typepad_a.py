from . import *

@profiledParser
class TypepadParserA( BlogParser ):        
    map_glob = '*/[0-9][0-9][0-9][0-9]/*/*.html'
    map_include = 'index.html'

