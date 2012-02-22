import os
import random
import datetime
import glob
import csv
from copy import deepcopy

log_path = '/users/agong/Desktop/blog-crawl-results/'
log_url = "http://www.cscs.umich.edu/~agong/blog-crawl-results/"

log_file = log_path+'inspector_logs.txt'

class Inspector(object):
    def __init__(self, blog_list=None, parser_registry=None):
        if blog_list:
            self.set_blog_list(blog_list)

        if parser_registry:
            self.set_parser_registry(parser_registry)

    def set_parser_registry(self, parser_registry):
        self.parser_registry = deepcopy(parser_registry)

    def set_blog_list(self, blog_list, shuffle=False, max_blogs=None):
        self.blog_list = deepcopy( blog_list )

        if shuffle:
            random.shuffle(self.blog_list)
            
        if max_blogs:
            self.blog_list = self.blog_list[:max_blogs]

    def init_csv_writer(self, slug, log_path=log_path, header=None):
        G = glob.glob(log_path+slug+'*.csv')
        filename = log_path+slug+str(len(G)+1)+'.csv'
        file_url = log_url+slug+str(len(G)+1)+'.csv'
        C = csv.writer(file(filename, 'w'))

        if header:
            C.writerow(header)

        return (filename, file_url, C)



class MapperInspector(Inspector):
    def inspect_blog_mapper_pair(self, blog, parser):
        P = self.parser_registry[parser]()
        posts = P.mapPostFiles(blog)
        return len(posts)
        
    def count_blog_files(self, blog):
        count = 0
        for root, subFolders, files in os.walk(blog):
            for file in files:
                count += 1
        return count

    def inspect(self, parsers=None, log_results=False):
        if not parsers:
            parsers = self.parser_registry.keys()

        if log_results:
            start_time = datetime.datetime.now()
            (filename, file_url, C) = self.init_csv_writer(
                    slug='mapper-inspector',
                    header=['index', 'file_count'] +
                        [p for p in parsers] +
                        ['blog', 'filepath', 'timestamp'],
                )

        for (i,blog) in enumerate(self.blog_list):
            results = {}
            for p in parsers:#self.parser_registry:
                results[p] = self.inspect_blog_mapper_pair(blog, p)

            row = [i, self.count_blog_files(blog)] + [results[p] for p in parsers] + \
                [
                    blog.split('/')[-1],
                    blog,
                    datetime.date.strftime(datetime.datetime.now(), "%Y/%m/%d %H:%M:%S")
                ]
            print '\t'.join([str(r) for r in row])

            if log_results:
                C.writerow( row )


        if log_results:
            log_line = "\t".join([
                self.__class__.__name__,
                datetime.date.strftime(start_time, "%Y/%m/%d %H:%M:%S"),
                datetime.date.strftime(datetime.datetime.now(), "%Y/%m/%d %H:%M:%S"),
                filename,
                str(len(self.blog_list)),
            ])

            print '='*80
            print 'Logged:\t', log_line
            print 'Output:\t', file_url
            
            logger = file(log_file, 'ab')
            logger.write('\n'+log_line)


"""
class ParserInspector(Inspector):

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



    #! This function is halfway there!
    def inspect(self, shuffle=False, max_posts=20,
        verbose=False, log_results=False, detailed_log=False, exceptions=None):
        
        if log_results:
            very_start_time = datetime.datetime.now()
            header = ['start_time', 'blog', 'post_count' ] +
                [ f+"_fields" for f in field_keys] +
                [ f+"_cleaners" for f in field_keys]

            (filename, file_url, C) = self.init_csv_writer(
                    slug='parser-inspector',
                    header=header,
                )
        
        if detailed_log:
            pass
#            header = ['blog', 'post_file' ]
#            for f in field_keys:
#                header +=  [ f+"_matchers", f+"_cleaners", f+"_result" ]
#            detailed_csv.writerow( header )


        for (i,blog) in enumerate(self.blog_list):
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

"""

class FrontPageInspector(Inspector):
    pass    


