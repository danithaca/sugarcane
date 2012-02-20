import subprocess

site_url = 'lowlywonk.blogspot.com'
blog_mirror_path = '/scratch/unmirrored2/agong/blog_crawl_2012-01/mirrors/'
log_file = '/scratch/unmirrored2/agong/blog_crawl_2012-01/logs/' + site_url + '.log'

logged = True

command_string = 'wget -mk http://'+site_url+' -w 5 -t 3 -T 30 -l 1 -P '+blog_mirror_path
#if logged: command_string += ' > ' + log_file
if logged: command_string += ' -o '+log_file

#print command_string
print site_url

p = subprocess.Popen( ["-c", command_string], shell=True )
p.wait()


"""
#command_string = 'wget -mk http://'+site_url+' -w 5 -t 3 -T 30 -P '+blog_mirror_path
#command_string = 'echo "blah blah blah"'
command_string = 'wget -mk http://'+site_url+' -w 5 -t 3 -T 30 -l 1 -P '+blog_mirror_path

command_list = command_string.split(' ')

if verbose:
    p = subprocess.Popen( command_list )
    p.wait()
else:
    p = subprocess.Popen( command_list, stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True) 
    p.wait()
    print 'Piped result:'
    print p.communicate()

"""
