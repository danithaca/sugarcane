import glob, csv, datetime, sys, inspect, random, os
#from blogParser import parser_registry, field_keys
#from blogParser import blogspot_a
#from blogParser.parsers import parser_registry, field_keys
from blogParser import parser_registry, field_keys
#from blogParser.utilities import firefox

input_path = '/scratch/unmirrored1/agong/blog_crawl_2012_01/mirrors/'
output_path = 'nothing-here-yet!!'
log_path = '/users/agong/Desktop/blog-crawl-results/'

log_url = "http://www.cscs.umich.edu/~agong/blog-crawl-results/"



#! This is all legacy code -- useful, but possibly not up to snuff ############

def check_one_parser(blog, parser):
    P = parser_registry[parser]()
    posts = P.mapPostFiles(blog)
    return len(posts)

def check_all_parsers(blog):
    results = {}
    for p in parser_registry:
        results[p] = check_one_parser(blog, p)

    return results

def test_mapper( blogs, parser, shuffle=False, max_blogs=None ):
    if shuffle:
        random.shuffle(blogs)
        
    if max_blogs:
        blogs = blogs[:max_blogs]

    for (i,blog) in enumerate(blogs):
        result = check_one_parser(blog, parser)
        row = [i, result, blog.split('/')[-1], blog, datetime.datetime.now()]
        print '\t'.join([str(r) for r in row])

def count_blog_files( blog ):
    count = 0#fileList = []
#    rootdir = blog#sys.argv[1]
    for root, subFolders, files in os.walk(blog):
        for file in files:
            count += 1#fileList.append(os.path.join(root,file))
    return count


#! End legacy code ############################################################

def test_parser_on_blog_list( parser, blogs, detailed_csv=None, summary_csv=None, k=20, verbose=False, shuffle=False ):
    if detailed_csv:
        header = ['blog', 'post_file' ]
        for f in field_keys:
            header +=  [ f+"_matchers", f+"_cleaners", f+"_result" ]
        detailed_csv.writerow( header )
        
    if summary_csv:
        summary_csv.writerow( ['start_time', 'blog', 'post_count' ] + [ f+"_fields" for f in field_keys] + [ f+"_cleaners" for f in field_keys] )

    for b in blogs:
        start_time = datetime.datetime.now()
        P = parser.mapPostFiles(b)
        
        if verbose:
            print b
            print '\t', len(P), 'posts found'

        if shuffle:
            random.shuffle(P)
        
        #Set up an empty results object
        results = {}
        for f in field_keys: results[f] = [0,0]
        
        #Take up tothe first k posts of the blog
        for p in P[:k]:
            #Check fields against the parser
            result = parser.parsePost(file(p,'r').read(), check_only=True)

            #Store to csv
            if detailed_csv:
                row = [b, p]
                for f in field_keys:
                    row +=  [ result[f][0], result[f][1], result[f][2].__repr__()[:80] ]
                detailed_csv.writerow( row )
            
            #Compile results
            for f in result:
                if result[f][0] == 1: results[f][0] += 1
                if result[f][1]: results[f][1] += 1

        if verbose:
            for f in results:
                print '\t', f, ' '*(14-len(f)), results[f]

        #Store to csv
        if summary_csv:
            summary_csv.writerow( [ start_time, b, len(P) ] + [results[f][0] for f in field_keys] + [results[f][1] for f in field_keys] )


def test_parser_on_one_blog( parser, blog, break_on_mistake=False, max_posts=None ):
    posts = parser.mapPostFiles(blog)
    print len(posts), 'posts found'
    
    if max_posts:
        posts = posts[:max_posts]
    
    results = []
    found_mistake = False
    for p in posts:
        print '='*80
        print p
        text = file(p,'r').read()
        r = parser.parsePost(text, verbose=True, check_only=True)
        results.append( r )

        for k in r:
            print '\t', k, ':'+' '*(14-len(k)), r[k][0], '\t', r[k][1]
            if r[k][2]:
                print '\t\t', r[k][2][:80]

            if not r[k][1] in [True, None]:
                found_mistake = True

        if found_mistake and break_on_mistake:
            print "Opening in Firefox..."
            firefox(p)
            return 0

        print

    #If all the posts parsed correctly, show the results, by field
    for f in field_keys:
        print '===', f, '========================================='
        for r in results:
            print r[f][2].__repr__()[:80]

    print '='*80
    
    #Parse the whole blog and save as xml
    xml = parser.parseBlog(blog, filename=log_path+"temp.xml", max_posts=max_posts)
    print log_url+"temp.xml"
#    firefox(log_path+"temp.xml")

    #Also convert and save as html
    parser.convertToHtml(xml, filename=log_path+"temp.html")
    print log_url+"temp.html"
#    firefox(log_path+"temp.html")
    


    return 1

def test_all_mappers( blogs, store_results=False, shuffle=False, max_blogs=None ):
    if store_results:
        G = glob.glob(log_path+'map-test-*.csv')
        C = csv.writer(file(log_path+'map-test-'+str(len(G)+1)+'.csv', 'w'))
        C.writerow( ['index', 'file_count'] + [p for p in parser_registry] + ['blog', 'filepath', 'timestamp'] )

    if shuffle:
        random.shuffle(blogs)
        
    if max_blogs:
        blogs = blogs[:max_blogs]

    print '\t'.join(['index', 'file_count']+[p for p in parser_registry])

    for (i,blog) in enumerate(blogs):
        results = check_all_parsers(blog)
        row = [i, count_blog_files(blog)] + [results[p] for p in parser_registry] + \
            [
                blog.split('/')[-1],
                blog,
                datetime.date.strftime(datetime.datetime.now(), "%Y/%m/%d %H:%M:%S")
            ]
        print '\t'.join([str(r) for r in row])
#        print '\t'.join( [str(r) for r in [i] + [results[p] for p in parser_registry] + [blog.split('/')[-1]] ])

        if store_results:
            C.writerow( row )

def list_parsers():
    print '=== Registered parsers: ==='
    for p in parser_registry:
        print '\t', p

##### Main function ###########################################################


def main(argv=None):

#    blogs = file('data/um1-completed-blogs.txt','r').read()[:-1].split('\n')
#    blogs = file('data/um1-blogspot-blogs.txt','r').read()[:-1].split('\n')
    blogs = file('data/um1-wordpress-blogs.txt','r').read()[:-1].split('\n')
#    print "\n".join(blogs[:5])

    command = argv[1]
    if command=='list-parsers':
        list_parsers()

    elif command=='test-all-mappers':
        test_all_mappers(blogs)

    elif command=='test-mapper':
        test_mapper(blogs, argv[2])

    elif command=='test-1x1':
        test_parser_on_one_blog(parser_registry[argv[2]](), input_path+argv[3], break_on_mistake=True)#, max_posts=20)

    elif command=='test-1xMany':
        test_parser_on_blog_list(
            parser_registry[argv[2]](),
            blogs,
            verbose=True,
            detailed_csv = csv.writer(file(log_path+'check_'+argv[2]+'.csv', 'w')),
            summary_csv = csv.writer(file(log_path+'/check_'+argv[2]+'_summary.csv', 'w')),
        )


    else:
        print 'Unknown command :', command
#        print blogs[:5]
#        for b in blogs:
#            print count_blog_files(b), b

    return 0

if __name__=='__main__':
    status = main(sys.argv)
    sys.exit(status)


