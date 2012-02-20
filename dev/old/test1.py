import glob
import lxml.etree as etree

import blogParser.utilities as util
import blogParser.parsers as parsers

### Main script ###
path = '/home/agong/Documents/blog_profiler/pol_blog_front_pages_2012-01-03/suffixed_files/'

xpath = {
    'post1' : '//div[@class="post-outer"]',
    'post2' : '//div[@id="main2"]/div[@class="post"]',
}

F = glob.glob( path+'*' )
F2 = util.filterByRegex( F, 'blogspot' )

#F3 = [f for f in F2 if util.countXpathMatches(f, xpath["post1"]) == 0]
#print len(F3)

results = [(
        util.countXpathMatches( f, xpath["post1"] ),
        util.countXpathMatches( f, xpath["post2"] )
    ) for f in F2]

for (x,y) in results[60:80]:
    print x, '\t', y

crosstabs = [[0,0],[0,0]]
for (x,y) in results:
    crosstabs[x>0][y>0] += 1
print crosstabs
#util.firefox(F3[1])

"""
F3 = util.filterBy
f = F[0]
#print f
#firefox( f )
#print countXpathMatches( f, "//a" )

for f in F[:20]:
    print util.countXpathMatches( f, '//div[@class="post-outer"]' )

#for f in F2[:200]:
#    print f in F, countXpathMatches( f, '//div[@class="post-outer"]' )

"""