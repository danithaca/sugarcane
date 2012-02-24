import os
import random
import datetime
import glob
import csv
from copy import deepcopy
from blogParser import field_keys, parser_registry

log_path = '/users/agong/Desktop/blog-crawl-results/'
log_url = "http://www.cscs.umich.edu/~agong/blog-crawl-results/"
log_file = log_path+'inspector_logs.txt'

blog_file_url = "http://www.cscs.umich.edu/~agong/um1-blog-crawl/"+"mirrors/"

class Inspector(object):
    def __init__(self, blog_list=None):
        if blog_list:
            self.set_blog_list(blog_list)

    def set_blog_list(self, blog_list, shuffle=False, max_blogs=None):
        self.blog_list = deepcopy( blog_list )

        if shuffle:
            random.shuffle(self.blog_list)
            
        if max_blogs:
            self.blog_list = self.blog_list[:max_blogs]

    def init_csv_writer(self, slug=None, log_path=log_path, header=None):
        if not slug:
            slug = self.__class__.__name__+'-'
        G = glob.glob(log_path+slug+'*.csv')

        filename = log_path+slug+str(len(G)+1)+'.csv'
        file_url = log_url+slug+str(len(G)+1)+'.csv'

        C = csv.writer(file(filename, 'w'))
        if header:
            C.writerow(header)

        return (filename, file_url, C)



class MapperInspector(Inspector):
    def inspect_blog_mapper_pair(self, blog, parser):
        P = parser_registry[parser]()
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
            parsers = parser_registry.keys()

        if log_results:
            start_time = datetime.datetime.now()
            (filename, file_url, C) = self.init_csv_writer(
#                    slug='mapper-inspector',
                    header=['index', 'file_count'] +
                        [p for p in parsers] +
                        ['blog', 'filepath', 'timestamp'],
                )

        for (i,blog) in enumerate(self.blog_list):
            results = {}
            for p in parsers:
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
            print 'Output:\t', file_url


class ParserInspector(Inspector):
    """
    def calc_xpath_success(self, results, field):
        success = 0
        for post in results:
#            print results[post][field][0:2]
            if results[post][field][0] == 1:
                success += 1 
        return success

    def calc_cleaner_success(self, results, field):
        success = 0
        for post in results:
            if results[post][field][1]:
                success += 1 
        return success

    def calc_percent_perfect(self, results):
        success = 0
        for post in results:
            good = True
            for f in field_keys:
                if not results[post][f][0] == 1:
                    good = False
                if not results[post][f][1] == True:
                    good = False

            if good:
                success += 1

        if len(results) > 0:
            return float(success)/len(results)
        else:
            return -1
    """
    def calc_success_rate(self, results, field):
        success = 0
        for post in results:
            if results[post][field]["success"]:
                success += 1 
        return success

    def calc_percent_perfect(self, results):
        success = 0
        for post in results:
            good = True
            for f in field_keys:
                if not results[post][f]["success"]:
                    good = False

            if good:
                success += 1

        if len(results) > 0:
            return float(success)/len(results)
        else:
            return -1

    def inspect_blog_parser_pair(self, blog, parser, max_posts, shuffle):
        P = parser_registry[parser]()
        (results, xml) = P.parseBlog(blog, max_posts=max_posts, shuffle=shuffle)
        return results

    def inspect(self, parsers=None, log_results=False, log_summary=False,
        shuffle=False, max_posts=20):
        
        if not parsers:
            parsers = parser_registry.keys()

        if log_results:
            start_time = datetime.datetime.now()
            
            #Initialize the blog-by-parser csv
            header = ['index'] + \
                ['post_count'] + \
                [f for f in field_keys] + \
                ['pct_perfect'] + \
                ['parser', 'blog', 'filepath', 'timestamp']
            (bxp_filename, bxp_file_url, bxp_csv) = self.init_csv_writer(slug="ParserInspector-BxP-",header=header)

        if log_summary:
            #Initialize the blog csv
            header = ['index'] + \
                ["best_parser", "best_pct"] + \
                ["post_count_"+p for p in parsers] + \
                ["perfect_pct_"+p for p in parsers] + \
                ['blog', 'filepath', 'timestamp']
            (summary_filename, summary_file_url, summary_csv) = self.init_csv_writer(slug="ParserInspector-summary-",header=header)

        for (i,blog) in enumerate(self.blog_list):
            post_count = {}
            perfect_pct = {}

            for p in parsers:
                results = self.inspect_blog_parser_pair(blog, p, max_posts, shuffle)
                post_count[p] = len(results)
                perfect_pct[p] = self.calc_percent_perfect(results)

                if log_results:
                    row = [i] + \
                        [post_count[p]] + \
                        [self.calc_success_rate(results, f) for f in field_keys] + \
                        [perfect_pct[p] ] + \
                        [
                            p,
                            blog.split('/')[-1],
                            blog,
                            datetime.date.strftime(datetime.datetime.now(), "%Y/%m/%d %H:%M:%S")
                        ]
                    bxp_csv.writerow( row )

#                    print '\t'.join([str(r) for r in row])

            if log_summary:
                best_parser = max(perfect_pct, key=perfect_pct.get)
                if perfect_pct[best_parser] <= 0:
                    best_parser = "None"
                    best_pct = -1
                else:
                    best_pct = perfect_pct[best_parser]
                    
                row = [i] + \
                    [best_parser, best_pct] + \
                    [post_count[p] for p in parsers] + \
                    [perfect_pct[p] for p in parsers] + \
                    [
                        blog.split('/')[-1],
                        blog,
                        datetime.date.strftime(datetime.datetime.now(), "%Y/%m/%d %H:%M:%S")
                    ]
                summary_csv.writerow( row )
                print '\t'.join([str(r) for r in row])

        if log_results:
            print 'Results file:\t', bxp_file_url

        if log_summary:
            print 'Summary file:\t', summary_file_url


class SoloBlogInspector(Inspector):

    def __init__(self, blog_path, blog_url):
        self.blog_path = blog_path
        self.blog_url = blog_url

#        #! A bit hacky here: SoloBlogInspector uses a "list" of one blog
#        self.set_blog_list([blog_path+blog_url])

    def inspect(self, parser_name, log_results=False,
        shuffle=False, max_posts=20,
        break_on_mistake=True):

        parser = parser_registry[parser_name]()
        blog = self.blog_path+self.blog_url    

        posts = parser.mapPostFiles(blog)
        print len(posts), 'posts found'
        
        if shuffle:
            random.shuffle(posts)
        
        if max_posts:
            posts = posts[:max_posts]
        
        results = []
        found_mistake = False
        for p in posts:
            print '='*80
            print p
            print blog_file_url + self.blog_url + p.split(self.blog_url)[1]
            text = file(p,'r').read()
            (r, x) = parser.parsePost(text, verbose=True)
            results.append( r )

            for f in r:
                print '\t', f, ':'+' '*(14-len(f)), r[f]["success"], '\t', r[f]["message"]

                if not r[f]["success"]:
                    found_mistake = True

            if found_mistake and break_on_mistake:
                print "Found mistake.  Exiting..."
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


"""
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


