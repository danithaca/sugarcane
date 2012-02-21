from . import *

@profiledParser
class NewsvineParserA( BlogParser ):        
    map_glob = '*/[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]/*/*'
    map_exclude = '(\?threadId)|(\?commentId)'


