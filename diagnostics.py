import glob, csv, datetime, sys, inspect, random, os, argh
from blogParser import parser_registry, field_keys
from blogParser.utilities import firefox
from blogInspector import MapperInspector

input_path = '/scratch/unmirrored1/agong/blog_crawl_2012_01/mirrors/'
output_path = 'nothing-here-yet!!'

default_blog_file = 'data/blog-short-list.txt'

#@argh.command
def list_parsers(args):
    "List registered parsers"
    for p in parser_registry:
        print '\t', p

"""
@argh.command
def test_mappers(blog_file=default_blog_file,
                 parsers=None,
                 log_results=False):
    "Test mappers from one or more parsers on a list of blogs"

    blogs = file(blog_file,'r').read()[:-1].split('\n')
    inspector = MapperInspector(blogs, parser_registry)
    inspector.inspect(parsers, log_results)
"""

#! The parsers command-line parameter doesn't work yet.  Use the default or die.
@argh.arg('--parsers', default=None, help='List of parsers')
@argh.arg('--log-results', default=False, help='Log the results to csv?')
@argh.arg('--blog-file', default=default_blog_file, help='A file containing the list of blogs on separate rows')
def test_mappers(args):
    "Test mappers from one or more parsers on a list of blogs"
    blogs = file(args.blog_file,'r').read()[:-1].split('\n')
    inspector = MapperInspector(blogs, parser_registry)
    inspector.inspect(args.parsers, args.log_results)
    


##### Main function ###########################################################

def main(argv=None):
    p = argh.ArghParser()
    p.add_commands([list_parsers, test_mappers])#,test-mappers])
    p.dispatch()

"""
#    blogs = file('data/um1-completed-blogs.txt','r').read()[:-1].split('\n')
#    blogs = file('data/um1-blogspot-blogs.txt','r').read()[:-1].split('\n')
#    blogs = file('data/um1-wordpress-blogs.txt','r').read()[:-1].split('\n')
    blogs = file('data/blog-short-list.txt','r').read()[:-1].split('\n')
#    print "\n".join(blogs[:5])

    command = argv[1]
    if command=='list-parsers':
        list_parsers()

    elif command=='test-all-mappers':
        inspector = MapperInspector(blogs, parser_registry)
        inspector.inspect(log_results=True)
#        test_all_mappers(blogs)

    else:
        print 'Unknown command :', command
#        print blogs[:5]
#        for b in blogs:
#            print count_blog_files(b), b

    return 0
"""
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


