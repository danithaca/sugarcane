#Multi script
import snowcrawl, time, re

def myUrlProcesser( (url, params) ):
    (text, download_stats) = snowcrawl.downloadUrl( 'http://'+url )
    (kept, classify_stats) = (0, [])
    (edges, edge_stats) = snowcrawl.findEdges( url, text )
    if kept:
        return (kept, text, edges, edges, download_stats + classify_stats + edge_stats)
    else:
        return (kept, text, [], edges, download_stats + classify_stats + edge_stats)

def noneLeft(self):
    return self.urls_remaining == 0

if __name__ == '__main__':
#    file_path = '/scratch/scratch2/agong/'
    file_path = '/home/agong/Documents/blog_profiler/'
    my_path = file_path+'pol_blog_front_pages_2012-01-03/'

    my_params = snowcrawl.Parameters(
        time_inc = 5,
        time_limit = 5,
        wave_size = 1000,
        save_states=False, save_files=True, save_edges=False,
        prioritize_urls = False,
        csv_header = ["download_start_time", "download_end_time", "length",
            "classify_start_time", "classify_end_time", "characters", "tokens",
            "edge_start_time", "edge_end_time", "out_degree", "self_loops"
        ],
        process_url_function = myUrlProcesser,
        decide_terminate_function = noneLeft
    )
    my_seed_list = file('blogger_survey_wave2_mturk_sample.txt', 'r').read().split('\n')[:-1]

    my_crawl = snowcrawl.MultiCrawler( pool_size=20 )
    my_crawl.runUntilDone( my_path, my_params, seed_list=my_seed_list, overwrite_existing_files=True )
    
    
