import glob, os, shutil, csv

path = '/home/agong/Documents/blog_profiler/pol_blog_front_pages_2012-01-03/'

g = path+'files/wave1/*'
#print g
F = glob.glob(g)

table = {}

#print len(F)
for f in F:
    stat_buf = os.stat(f)
    if stat_buf.st_size/1024 > 0:
        fname = path+'suffixed_files/'+f.split('/')[-1]+'.html'
        shutil.copyfile(f, fname)

