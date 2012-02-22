import glob, csv, datetime, sys, inspect, random, os, argh
from blogParser import parser_registry, field_keys
#from blogParser.utilities import firefox
from blogInspector import MapperInspector, ParserInspector

input_path = '/scratch/unmirrored1/agong/blog_crawl_2012_01/mirrors/'
output_path = 'nothing-here-yet!!'
default_blog_file = 'data/blog-short-list.txt'

def list_parsers(args):
    "List registered parsers"
    for p in parser_registry:
        print '\t', p

@argh.arg('--parsers', default=None, help='List of parsers', nargs='+')
@argh.arg('--blog-file', default=default_blog_file, help='A file containing the list of blogs on separate rows')
@argh.arg('--log-results', default=False, help='Log the results to csv?')
def test_mappers(args):
    "Test mappers from one or more parsers on a list of blogs"
    
    blogs = file(args.blog_file,'r').read()[:-1].split('\n')
    inspector = MapperInspector(blogs, parser_registry)
    inspector.inspect(args.parsers, args.log_results)

#! The wrapper functions for various inspectors are reduntant.
#  This could mostly be rewritten as a decorator
#  Not worth the time right now.
@argh.arg('--parsers', default=None, help='List of parsers', nargs='+')
@argh.arg('--blog-file', default=default_blog_file, help='A file containing the list of blogs on separate rows')
@argh.arg('--log-results', default=False, help='Log blog-by-parser results to csv?')
@argh.arg('--log-summary', default=False, help='Log blog-level summary results to csv?')
def test_parsers(args):
    "Test one or more parsers on a list of blogs"
    
    blogs = file(args.blog_file,'r').read()[:-1].split('\n')
    inspector = ParserInspector(blogs, parser_registry)
    inspector.inspect(args.parsers, log_results=args.log_results, log_summary=args.log_summary)




##### Main function ###########################################################

def main(argv=None):
    p = argh.ArghParser()
    p.add_commands([list_parsers, test_mappers, test_parsers])
    p.dispatch()

"""
    elif command=='test-mapper':
        test_mapper(blogs, argv[2])

    elif command=='test-1x1':
        test_parser_on_one_blog(parser_registry[argv[2]](), input_path+argv[3], break_on_mistake=True, max_posts=20)

    elif command=='test-1xMany':
        test_parser_on_blog_list(
            parser_registry[argv[2]](),
            blogs,
            verbose=True,
            detailed_csv = csv.writer(file(log_path+'check_'+argv[2]+'.csv', 'w')),
            summary_csv = csv.writer(file(log_path+'/check_'+argv[2]+'_summary.csv', 'w')),
        )
"""

if __name__=='__main__':
    status = main(sys.argv)
    sys.exit(status)


