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

    def inspect(self, log_results=False):
        if log_results:
            start_time = datetime.datetime.now()
            (filename, file_url, C) = self.init_csv_writer(
                    slug='mapper-inspector',
                    header=['index', 'file_count'] +
                        [p for p in self.parser_registry] +
                        ['blog', 'filepath', 'timestamp'],
                )

        for (i,blog) in enumerate(self.blog_list):
            results = {}
            for p in self.parser_registry:
                results[p] = self.inspect_blog_mapper_pair(blog, p)

            row = [i, self.count_blog_files(blog)] + [results[p] for p in self.parser_registry] + \
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
            logger.write(log_line)



class ParserInspector(Inspector):
    def inspect(self, shuffle=False, max_posts=20,
        verbose=False, log_results=False, exceptions=None):
        pass



