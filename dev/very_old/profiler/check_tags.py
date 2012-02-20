import glob, re, os, csv, random

def removeDupes(L):
	L2 = []
	for l in L:
		if not l in L2: L2.append(l)
	return(L2)

def getClassAndIdTags( f ):
	#Find all class tags
	D = re.findall("class=[\"'](.+?)[\"']", file(f,'r').read())
	C = []
	for d in D: C += d.split(' ')

	#Find all id tags
	I = re.findall("id=[\"'](.*?)[\"']", file(f,'r').read())

	return(C,I)


##############################################################################

F = glob.glob('/scratch/scratch2/agong/pol_blog_front_pages_10.20.2011/files/wave*/*')
print 'Total matches:', len(F)

common_tags = file('common_tags.txt','r').read().split('\n')
#tags = ['post-outer','type-post','entry-header','asset-header', 'main_column', 'form-text']
tags = []#'content-wrapper', 'type-post']

my_csv = csv.writer(file('tag_output.csv','w'))
my_csv.writerow( ['url', 'filename'] + tags )

#tag_csv = csv.writer(file('blog_tag_matrix.csv','w'))
#tag_csv.writerow( ['url', 'filename'] + common_tags )

matched_pages = []
unmatched_pages = []
mmatched_pages = []

matched_tags = []
unmatched_tags = {}

print 'Matching...'
random.shuffle(F)

count = 0
for f in F:
	count+=1
	(C,I) = getClassAndIdTags(f)

	U = f.split('/')[-1]
	R = [int(t in C+I) for t in tags]
	my_csv.writerow( [U, f] + R )
	#tag_csv.writerow( [U, f] + [int(t in C+I) for t in common_tags] )

	if sum(R) == 1:
		matched_pages.append( f )
		for t in removeDupes(C+I):
			if not t in matched_tags: matched_tags.append(t)

	if sum(R) > 1:
		print R, '\t', U
		mmatched_pages.append( f )

	if sum(R) == 0:
		unmatched_pages.append( f )
		for t in removeDupes(C+I):
			if not t in matched_tags:
				if t in unmatched_tags: unmatched_tags[t] +=1
				else: unmatched_tags[t] = 1

	if not count%100: print count

##############################################################################

"""
for t in unmatched_tags:
	if unmatched_tags[t] > 50:
		print str(unmatched_tags[t]) + '\t' + t
"""

print "Matched pages:", len(matched_pages)
print "Unmatched pages:", len(unmatched_pages)
print "Multiple matched pages:", len(mmatched_pages)
print
print "Matched tags:", len(matched_tags)
print "Unmatched tags:", len(unmatched_tags)


#print "Common tags:", sum([ int(unmatched_tags[x]>100) for x in unmatched_tags])
#common_tags = []
#for t in unmatched_tags:
#	if unmatched_tags[t]>20:
#		common_tags.append(t)
#file('common_tags.txt','w').write('\n'.join(common_tags))


