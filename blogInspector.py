import os
import random
import datetime
import glob
import csv

from collections import defaultdict
from copy import deepcopy
from lxml import html, etree

from blogParser import field_keys, parser_registry

log_path = '/users/agong/Desktop/blog-crawl-results/'
log_url = "http://www.cscs.umich.edu/~agong/blog-crawl-results/"
log_file = log_path+'inspector_logs.txt'

blog_file_url = "http://www.cscs.umich.edu/~agong/um1-blog-crawl/"+"mirrors/"

#! Hardcoded for now.
required_fields = ['content']#['title', 'date', 'content']


class Inspector(object):
    def __init__(self, blog_path, blog_list=None):
        self.blog_path = blog_path
    
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
            slug = self.__class__.__name__

#        G = glob.glob(log_path+slug+'*.csv')
#        filename = log_path+slug+str(len(G)+1)+'.csv'
#        file_url = log_url+slug+str(len(G)+1)+'.csv'

        filename = log_path+slug+'.csv'
        file_url = log_url+slug+'.csv'

        C = csv.writer(file(filename, 'w'))
        if header:
            C.writerow(header)

        return (filename, file_url, C)



class MapperInspector(Inspector):
    def inspect_blog_mapper_pair(self, blog, parser):
        P = parser_registry[parser]()
        posts = P.mapPostFiles(self.blog_path+blog)
        return len(posts)
        
    def count_blog_files(self, blog):
        count = 0
        for root, subFolders, files in os.walk(self.blog_path+blog):
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
                    blog,#.split('/')[-1],
                    self.blog_path+blog,
                    datetime.date.strftime(datetime.datetime.now(), "%Y/%m/%d %H:%M:%S")
                ]
            print '\t'.join([str(r) for r in row])

            if log_results:
                C.writerow( row )

        if log_results:
            print 'Output:\t', file_url


class ParserInspector(Inspector):
    def calc_success_rate(self, results, field):
        success = 0
#        print results
        for post in results:
#            print results[post][field]
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

    def calc_percent_acceptable(self, results):    
        success = 0
        for post in results:
            good = True
            for f in required_fields:
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
        (results, xml) = P.parseBlog(self.blog_path+blog, max_posts=max_posts, shuffle=shuffle)
        return results

    def inspect(self, parsers=None, log_results=False, log_summary=False,
        shuffle=False, max_posts=20, verbose=False):
        
        if not parsers:
            parsers = parser_registry.keys()

        if log_results:
            start_time = datetime.datetime.now()
            
            #Initialize the blog-by-parser csv
            header = ['index'] + \
                ['post_count'] + \
                ['pct_perfect', 'pct_acceptable'] + \
                [f for f in field_keys] + \
                ['parser', 'blog', 'filepath', 'timestamp']
            (bxp_filename, bxp_file_url, bxp_csv) = self.init_csv_writer(slug="ParserInspector-BxP",header=header)

        if log_summary:
            #Initialize the blog csv
            header = ['index'] + \
                ["best_parser", "best_pct"] + \
                [p+"_post_count" for p in parsers] + \
                [p+"_pct_perfect" for p in parsers] + \
                [p+"_pct_acceptable" for p in parsers] + \
                ['blog', 'filepath', 'timestamp']
            (summary_filename, summary_file_url, summary_csv) = self.init_csv_writer(slug="ParserInspector-summary",header=header)

        acceptable_matches = 0

        for (i,blog) in enumerate(self.blog_list):
            post_count = {}
            perfect_pct = {}
            acceptable_pct = {}

            for p in parsers:
                results = self.inspect_blog_parser_pair(blog, p, max_posts, shuffle)
                post_count[p] = len(results)
                perfect_pct[p] = self.calc_percent_perfect(results)
                acceptable_pct[p] = self.calc_percent_acceptable(results)

                if log_results:
                    row = [i] + \
                        [post_count[p]] + \
                        [perfect_pct[p] ] + \
                        [acceptable_pct[p] ] + \
                        [self.calc_success_rate(results, f) for f in field_keys] + \
                        [
                            p,
                            blog,#.split('/')[-1],
                            self.blog_path+blog,
                            datetime.date.strftime(datetime.datetime.now(), "%Y/%m/%d %H:%M:%S")
                        ]
                    bxp_csv.writerow( row )

#                    print '\t'.join([str(r) for r in row])

            if log_summary:
                best_parser = max(acceptable_pct, key=acceptable_pct.get)
                if acceptable_pct[best_parser] <= 0:
                    best_parser = "None"
                    best_pct = -1
                else:
                    best_pct = acceptable_pct[best_parser]
                    
                    if best_pct == 1:
                        acceptable_matches += 1
                    
                row = [i] + \
                    [best_parser, best_pct] + \
                    [post_count[p] for p in parsers] + \
                    [perfect_pct[p] for p in parsers] + \
                    [acceptable_pct[p] for p in parsers] + \
                    [
                        blog,#.split('/')[-1],
                        self.blog_path+blog,
                        datetime.date.strftime(datetime.datetime.now(), "%Y/%m/%d %H:%M:%S")
                    ]
                summary_csv.writerow( row )
                print '\t'.join([str(r) for r in row])

        print '='*80
        print acceptable_matches, 'acceptable matches'
        print len(self.blog_list), 'total blogs checked'
        print float(acceptable_matches)/len(self.blog_list), 'percent success'
        print 
        
        if log_results:
            print 'Results file:\t', bxp_file_url

        if log_summary:
            print 'Summary file:\t', summary_file_url



class SoloBlogInspector(ParserInspector):

    def __init__(self, blog_path, blog_url):
        self.blog_path = blog_path
        self.blog_url = blog_url
        
    def inspect_multiple(self, parsers=None, shuffle=False, max_posts=20, verbose=False):
        "Check parsers and see which one seems to fit the best."
            
        if not parsers:
            parsers = parser_registry.keys()
        
        post_count = {}
        perfect_pct = {}
        acceptable_pct = {}

        for p in parsers:
            results = self.inspect_blog_parser_pair(self.blog_url, p, max_posts, shuffle)
#            print results
            post_count[p] = len(results)
            perfect_pct[p] = self.calc_percent_perfect(results)
            acceptable_pct[p] = self.calc_percent_acceptable(results)

            print p
            print '\t', post_count[p], '\tPost count'
            print '\t', round(100*perfect_pct[p]), '\t% perfect'
            print '\t', round(100*acceptable_pct[p]), '\t% acceptable'
            print
            for f in field_keys:
                print '\t', self.calc_success_rate(results, f), f

            print

        best_parser = max(acceptable_pct, key=acceptable_pct.get)
        if acceptable_pct[best_parser] <= 0:
            best_parser = "None"
            best_pct = -1
        else:
            best_pct = acceptable_pct[best_parser]
                    
        print
        print best_parser, ':', round(100*best_pct)

    def inspect_single(self, parser_name, log_results=False,
        shuffle=False, max_posts=20,
        break_on_mistake=True, break_on_any_mistake=False):

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
                    if break_on_any_mistake:
                        found_mistake = True
                        
                    if break_on_mistake and f in required_fields:
                        found_mistake = True

            if found_mistake and break_on_mistake:
                print "Found mistake.  Exiting..."
                return 0

            print

        #If all the posts parsed correctly, show the results, by field
        for f in field_keys:
            print '===', f, '========================================='
            for r in results:
                print r[f]["contents"].__repr__()[:80]

        print '='*80
        
        #Parse the whole blog and save as xml
        (result, xml) = parser.parseBlog(blog, filename=log_path+"temp.xml", max_posts=max_posts)
        print log_url+"temp.xml"

        #Also convert and save as html
        parser.convertToHtml(xml, filename=log_path+"temp.html")
        print log_url+"temp.html"
        
        return 1


class XpathInspector(Inspector):
    """Quick comparison of blogs to xpath queries -- no need for Parser classes."""
    
    def inspect(self, xpath_queries, mapper_parser=None):
        matches = defaultdict(int)
    
        for blog in self.blog_list:
            try:
                html_parser = etree.HTMLParser(remove_blank_text=True)
                html_tree = html.parse(self.blog_path + blog + '/index.html', html_parser)

                found_one = False
                for x in xpath_queries:
                    result = html_tree.xpath(x)
                    count = len(result)

                    if count > 0:
                        matches[x] += 1
                        found_one = True

                if not found_one:
                    print '='*80
                    print blog
                    print blog_file_url + blog + '/index.html'
                    print

            except IOError:
                print '='*80
                print 'IOError -- does this blog have an index.html file?'
                print blog
                print blog_file_url + blog + '/index.html'
                print
                    


        print
        print '='*80
        for x in xpath_queries:
            print matches[x], '\t', x


class FrontPageInspector(Inspector):
    pass
