#from /users/agong/my_stuff/my_projects/unfinished/iPhD/panel_crawl

import subprocess, time
from multiprocessing import Pool

"""
def get_site( site_url ):
#	print 'http://'+site_url
	command_string = 'wget -mk http://'+site_url+' -w 5 -t 3 -T 30 -P /scratch/unmirrored5/agong/blog_panel_crawl'
	command_string = command_string.split(' ')
	print command_string
	p = subprocess.Popen( command_string )
#		stdout=subprocess.PIPE, 
#		stderr=subprocess.PIPE, 
#		stdid=subprocess.PIPE)
	p.wait()
"""


def get_site( site_url ):
  log_start()
  
  log_finish()



blogs = file('blog_list.txt', 'r').read().split('\n')[:-1]

P = Pool( 100 )
R = P.map( get_site, blogs )

#get_site( blogs[0] )

