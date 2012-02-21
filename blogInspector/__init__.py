from copy import deepcopy

log_path = '/users/agong/Desktop/blog-crawl-results/'
log_url = "http://www.cscs.umich.edu/~agong/blog-crawl-results/"


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
        C = csv.writer(file(log_path+slug+str(len(G)+1)+'.csv', 'w'))

        if header:
            C.writerow(header)

        return C

    def inspect(self, shuffle=False, max_posts=20,
        log_results=False, exceptions=None):
        pass


class MapperInspector(Inspector):

    def inspect_blog_mapper_pair(self, blog, parser):
        P = self.parser_registry[parser]()
        posts = P.mapPostFiles(blog)
        return len(posts)

#    def inspect(self, shuffle=False, max_posts=20,
#        verbose=False, log_results=False, exceptions=None):

    def inspect(self, verbose=False, log_results=False, exceptions=None):
        if log_results:
            C = init_csv_writer(
                    slug='mapper-inspector'
                    header=['index', 'file_count'] +
                        [p for p in self.parser_registry] +
                        ['blog', 'filepath', 'timestamp'],
                )

#        print '\t'.join(['index', 'file_count']+[p for p in parser_registry])

        for (i,blog) in enumerate(self.blog_list):
            results = {}
            for p in self.parser_registry:
                results[p] = inspect_blog_mapper_pair(blog, p)

            row = [i, count_blog_files(blog)] + [results[p] for p in parser_registry] + \
                [
                    blog.split('/')[-1],
                    blog,
                    datetime.date.strftime(datetime.datetime.now(), "%Y/%m/%d %H:%M:%S")
                ]
            print '\t'.join([str(r) for r in row])

            if store_results:
                C.writerow( row )



class ParserInspector(Inspector):
    pass


