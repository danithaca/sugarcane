import re, glob, csv, random
import blog_parsers

	
def checkIfMatch( blog_path, blog_type ):
	#Depending on the blog type we are attempting to parse, search for different files.
	if blog_type == 'blogger':
		post_files = glob.glob( blog_path+'20[0-9][0-9]/*/*.html' )

	elif blog_type == 'wordpress':
		post_files = glob.glob( blog_path+'20[0-9][0-9]/[0-9][0-9]/[0-9][0-9]/*/index.html' )

	elif blog_type == 'typepad':
		post_files = glob.glob( blog_path+'*/20[0-9][0-9]/*/*.html' )
		good_post_files = []
		for p in post_files:
			if re.search ( 'index.html', p ) == None:
				good_post_files.append(p)	
		post_files = good_post_files

	elif blog_type == 'livejournal':
		post_files = glob.glob( blog_path+'20[0-9][0-9]/*/*/*.html' )

	elif blog_type == 'newsvine':
		post_files = glob.glob( blog_path+'_newsvine/20[0-9][0-9]/*/*/*' )
		good_post_files = []
		for p in post_files:
			if re.search ( '\?commentId', p ) == None and re.search ( '\?threadId', p ) == None:
				good_post_files.append(p)	
		post_files = good_post_files

	else:
		post_files = []


	print '\t', blog_type, '\t', len(post_files), 'files found'

	if len( post_files ) > 0:
		#Shuffle the posts at random
		random.shuffle( post_files )

		fails = 0
		#Loop over the first twenty posts
		for f in post_files[:20]:
			#Try to apply the appropriate parser
			try:
				x = post_parsers[blog_type](f)
				#If the parser succeeds, loop over the tags within the post xml
				for y in x:
					#Print the date tag
					if y.tag == 'date':
						print '\t\t', re.sub( '\n', ' ', y.text[:200] )
			#If the parser fails, add one to the fail count
			except:
				fails += 1

		print '\t\t', fails, 'of 20 failed to parse'
	print


	
#Read in a list of all the blogs
blog_list = file('blog_list.txt','rb').read().split('\r\n')[:50][:-1]

#Set the five blog types
blog_types = ['blogger', 'wordpress', 'typepad', 'livejournal', 'newsvine']

#Create a corresponding dictionary of blog post parsers
post_parsers = {'blogger':	blog_parsers.process_blogger_post,
	'wordpress': blog_parsers.process_wordpress_post,
	'typepad': blog_parsers.process_typepad_post,
	'livejournal': blog_parsers.process_livejournal_post,
	'newsvine': blog_parsers.process_newsvine_post}
	
#Loop over the list of blogs
for a in range(len(blog_list)):
	print a, blog_list[a]
	#Loop over blog types
	for t in blog_types:
		#Try to parse the blog by this type
		checkIfMatch( '/scratch/unmirrored5/agong/blog_panel_crawl/'+blog_list[a]+'/', t )
