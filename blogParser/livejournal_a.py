from . import *

@profiledParser
class LiveJournalParserA( BlogParser ):
    map_glob = '[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]/*.html'


