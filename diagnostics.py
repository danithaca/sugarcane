import glob, csv, datetime, sys, inspect, random, os, argh
from blogParser import parser_registry
#from blogParser.utilities import firefox
from blogInspector import MapperInspector, ParserInspector, SoloBlogInspector, XpathInspector

input_path = '/scratch/unmirrored1/agong/blog_crawl_2012_01/mirrors/'
output_path = 'nothing-here-yet!!'
default_blog_file = 'data/blog-short-list.txt'


def list_parsers(args):
    "List registered parsers"
    for p in parser_registry:
        print '\t', p


@argh.arg('--parsers', default=None, help='List of parsers', nargs='+')
@argh.arg('--blog-file', default=default_blog_file, help='A file containing the list of blogs on separate rows')
@argh.arg('--input-path', default=input_path, help='The path where the blog is stored')
@argh.arg('--log-results', default=False, help='Log the results to csv?')
def test_mappers(args):
    "Test mappers from one or more parsers on a list of blogs"
    
    blogs = file(args.blog_file,'r').read()[:-1].split('\n')
    inspector = MapperInspector(args.input_path, blogs)
    inspector.inspect(args.parsers, args.log_results)


#! The wrapper functions for various inspectors are redundant.
#  This could mostly be rewritten as a decorator
#  Not worth the time right now.
@argh.arg('--parsers', default=None, help='List of parsers', nargs='+')
@argh.arg('--blogs', default=None, help='List of blogs', nargs='+')
@argh.arg('--blog-file', default=default_blog_file, help='A file containing the list of blogs on separate rows')
@argh.arg('--input-path', default=input_path, help='The path where the blog is stored')
@argh.arg('--log-results', default=False, help='Log blog-by-parser results to csv?')
@argh.arg('--log-summary', default=False, help='Log blog-level summary results to csv?')
def test_parsers(args):
    "Test one or more parsers on a list of blogs"

    if args.blogs:    
        blogs = args.blogs
    else:
        blogs = file(args.blog_file,'r').read()[:-1].split('\n')
        
    inspector = ParserInspector(args.input_path, blogs)
    inspector.inspect(args.parsers, log_results=args.log_results, log_summary=args.log_summary)


@argh.arg('blog', help='The URL of the blog to be parsed')
@argh.arg('--parsers', default=None, help='List of parsers', nargs='+')
@argh.arg('--parser', default=None, help='The parser to test')
@argh.arg('--input-path', default=input_path, help='The path where the blog is stored')
@argh.arg('--shuffle', default=False, help='Shuffle posts?')
@argh.arg('--log-results', default=False, help='Log post-level results to csv?')
@argh.arg('--strict-breaking', default=False, help='Break on any mistake?')
def test_blog(args):
    "Test one or more parsers on a single blog (Workhorse inspector)"
    inspector = SoloBlogInspector(args.input_path, args.blog)
    if args.parser:
        inspector.inspect_single(
            args.parser,
            log_results=args.log_results,
            shuffle=args.shuffle,
            break_on_any_mistake=args.strict_breaking
            )
    else:
        inspector.inspect_multiple(args.parsers,
            shuffle=args.shuffle,
            )


#! This arg should probably be optional
#@argh.arg('blog_file', help='A file containing blog urls in rows')
@argh.arg('xpath_query_file', default=None, help='A file containing xpath queries in rows')
@argh.arg('--blog-file', default=default_blog_file, help='A file containing the list of blogs on separate rows')
@argh.arg('--input-path', default=input_path, help='The path where the blog is stored')
@argh.arg('--mapper', default=None, help='A parser contining a mapper to use for mapping posts')
def xpath_test(args):
    "Quick comparison of blogs to xpath queries"
    
    blogs = file(args.blog_file,'r').read()[:-1].split('\n')
    inspector = XpathInspector(args.input_path, blogs)
    
    xpath_queries = file(args.xpath_query_file,'r').read()[:-1].split('\n')
    
    inspector.inspect(xpath_queries, args.mapper)


@argh.arg('blog_file', help='A file containing blog urls in rows')
@argh.arg('--input-path', default=input_path, help='The path where the blog is stored')
@argh.arg('--mapper', default=None, help='A parser contining a mapper to use for mapping posts')
def scraper_test(args):
    "Quick test of scraper functions on a list of blogs"

    blogs = file(args.blog_file,'r').read()[:-1].split('\n')
    inspector = XpathInspector(args.input_path, blogs)
    
    xpath_queries = file(args.xpath_query_file,'r').read()[:-1].split('\n')
    
    inspector.inspect(xpath_queries, args.mapper)

##### Main function ###########################################################

def main(argv=None):
    p = argh.ArghParser()
    p.add_commands([list_parsers, test_mappers, test_parsers, test_blog, xpath_test])
    p.dispatch()

if __name__=='__main__':
    status = main(sys.argv)
    sys.exit(status)


