import glob
import re
import timeit
import lxml.html 
import profiler3

try:
	import lxml.etree as etree
except:
	import xml.etree.cElementTree as etree

##### Post processors ########################################################

def process_blogger_post( file_name, verbose = False):
	
	# Create xml entry

	post_xml = etree.Element( "post" )

	parser = etree.HTMLParser()
	tree = etree.parse( file_name , parser)

	doc = lxml.html.fromstring(open(file_name, 'r').read())

	try:

	# Grab main body
		result = doc.xpath("//div[@class='post-body entry-content']")

		if len(result) == 1:
			post_xml.text = etree.tostring( result[0], pretty_print=True)
		elif verbose:
			print 'Error: too many or too few divs match for main body for', file_name


	#Get length
	#e = etree.SubElement( post_xml, "length" )
	 	char = str(len(post_xml.text))	
	 	post_xml.set( "post_char", char)
	

	### Grab title
		resultTitle = doc.xpath("//h3[@class='post-title entry-title']")

		if len(resultTitle) == 1:
			e = etree.SubElement( post_xml, "title" )
			e.text = etree.tostring( resultTitle[0], pretty_print=True)
		elif verbose:
			print 'Error: too many or too few divs match for main body for', file_name


	### Grab date	
		resultDate = doc.xpath("//h2[@class='date-header']")

		if len(resultDate) == 1:
			e = etree.SubElement( post_xml, "date" )
			e.text = etree.tostring( resultDate[0], pretty_print=True)
		elif verbose:
			print 'Error: too many or too few divs match for main body for', file_name

	### Grab time (also grabs date and time within the xml tag <abbr>)
		resultTime = doc.xpath("//abbr[@class='published']")

		if len(resultTime) == 1:
			e = etree.SubElement( post_xml, "time" )
			e.text = etree.tostring( resultTime[0], pretty_print=True)
		elif verbose:
			print 'Error: too many or too few divs match for main body for', file_name

	### Grab labels
		resultLabels = doc.xpath("//span[@class='post-labels']")

		if len(resultLabels) == 1:
			e = etree.SubElement( post_xml, "labels" )
			e.text = etree.tostring( resultTime[0], pretty_print=True)
		elif verbose:
			print 'Error: too many or too few divs match for main body for', file_name


	### Grab number of comments
		resultNumComments = doc.xpath("h4")

		if len(resultNumComments) == 1:
			e = etree.SubElement( post_xml, "comments" )
			e.text = etree.tostring( resultTime[0], pretty_print=True)
		elif verbose:
			print 'Error: too many or too few divs match for main body for', file_name


	### Grab comments
		resultComments = doc.xpath("//dd[@class='comment-body']")

		if len(resultComments) == 1:
			e = etree.SubElement( post_xml, "time" )
			e.text = etree.tostring( resultTime[0], pretty_print=True)
		elif verbose:
			print 'Error: too many or too few divs match for main body for', file_name

	except:
		if verbose: "There was an error parsing the main body for", file_name
		pass

	return post_xml
	

def process_wordpress_post( file_name, verbose = False):
	# Create xml entry
	post_xml = etree.Element( "post" )
	
	parser = etree.HTMLParser()
	tree = etree.parse( file_name , parser)

	doc = lxml.html.fromstring(open(file_name, 'r').read())

	try: 

	# Grab main body (also gets some other html tags at the end (e.g. share this))
		result = doc.xpath("//div[@class='post-content']")

		if len(result) == 1:
			post_xml.text = etree.tostring( result[0], pretty_print=True)
		elif verbose:
			print 'Error: too many or too few divs match for main body for', file_name


	###Get length
		#e = etree.SubElement( post_xml, "length" )
		char = str(len(post_xml.text))	
		post_xml.set( "post_char", char)

	### Grab title
		resultTitle = doc.xpath("//div[@class='post-title']")

		if len(resultTitle) == 1:
			e = etree.SubElement( post_xml, "title" )
			e.text = etree.tostring( resultTitle[0], pretty_print=True)
		elif verbose:
			print 'Error: too many or too few divs match for main body for', file_name


	### Grab date
		resultDate = doc.xpath("//div[@class='date']")

		if len(resultDate) == 1:
			e = etree.SubElement( post_xml, "date" )
			e.text = etree.tostring( resultTitle[0], pretty_print=True)
		elif verbose:
			print 'Error: too many or too few divs match for main body for', file_name


	### Grab time - not an option in WP
		e = etree.SubElement( post_xml, "time" )

	### Grab categories
		resultCategories = doc.xpath("//div[@class='categories']")

		if len(resultCategories) == 1:
			e = etree.SubElement( post_xml, "categories" )
			e.text = etree.tostring( resultTitle[0], pretty_print=True)
		elif verbose:
			print 'Error: too many or too few divs match for main body for', file_name


	### Grab tags
		resultTags = doc.xpath("//div[@class='tags']")

		if len(resultTags) == 1:
			e = etree.SubElement( post_xml, "tags" )
			e.text = etree.tostring( resultTitle[0], pretty_print=True)
		elif verbose:
			print 'Error: too many or too few divs match for main body for', file_name
	

	### Grab number of comments
		resultNumComments = doc.xpath("//div[@class='comments']")

		if len(resultNumComments) == 1:
			e = etree.SubElement( post_xml, "numComments" )
			e.text = etree.tostring( resultTitle[0], pretty_print=True)
		elif verbose:
			print 'Error: too many or too few divs match for main body for', file_name

	except:
		if verbose: "There was an error parsing the main body for", file_name
		pass

	return post_xml

def process_typepad_post(file_name, verbose = False):
	# Create xml entry
	post_xml = etree.Element( "post" )
	
	parser = etree.HTMLParser()
	tree = etree.parse( file_name , parser)

	doc = lxml.html.fromstring(open(file_name, 'r').read())

	try:
	# Grab main body
		result = doc.xpath("//div[@class='entry-body']")

		if len(result) == 1:
			post_xml.text = etree.tostring( result[0], pretty_print=True)
		elif verbose:
			print 'Error: too many or too few divs match for main body for', file_name


	###Get length
		#e = etree.SubElement( post_xml, "length" )
		char = str(len(post_xml.text))	
		post_xml.set( "post_char", char)
	
	### Grab title
		resultTitle = doc.xpath("//div[@class='entry-header']")

		if len(resultTitle) == 1:
			e = etree.SubElement( post_xml, "title" )
			e.text = etree.tostring( resultTitle[0], pretty_print=True)
		elif verbose:
			print 'Error: too many or too few divs match for main body for', file_name


	### Grab date
		resultDate = doc.xpath("//div[@class='date-header']")

		if len(resultDate) == 1:
			e = etree.SubElement( post_xml, "date" )
			e.text = etree.tostring( resultTitle[0], pretty_print=True)
		elif verbose:
			print 'Error: too many or too few divs match for main body for', file_name


	### Grab time - not an option in TP
		e = etree.SubElement( post_xml, "time" )

	### Grab categories

		resultCategories = doc.xpath("//div[@class='post-footers']")

		if len(resultCategories) == 1:
			e = etree.SubElement( post_xml, "categories" )
			e.text = etree.tostring( resultTitle[0], pretty_print=True)
		elif verbose:
			print 'Error: too many or too few divs match for main body for', file_name


	### Grab number of comments - not an option in TP
		e = etree.SubElement( post_xml, "num_comments" )




	except:
		if verbose: "There was an error parsing the main body for", file_name
		pass

	return post_xml
	
def process_newsvine_post( file_name, verbose = False):
	# Create xml entry
	post_xml = etree.Element( "post" )
	
	parser = etree.HTMLParser()
	tree = etree.parse( file_name , parser)

	doc = lxml.html.fromstring(open(file_name, 'r').read())

	try:
	# Grab main body
		result = doc.xpath("//div[@class='articleText']")

		if len(result) == 1:
			post_xml.text = etree.tostring( result[0], pretty_print=True)
		elif verbose:
			print 'Error: too many or too few divs match for main body for', file_name

	###Get length
		#e = etree.SubElement( post_xml, "length" )
		char = str(len(post_xml.text))	
		post_xml.set( "post_char", char)
	
	### Grab title
		resultTitle = doc.xpath("//div[@class='gl_headline']")

		if len(resultTitle) == 1:
			e = etree.SubElement( post_xml, "title" )
			e.text = etree.tostring( resultTitle[0], pretty_print=True)
		elif verbose:
			print 'Error: too many or too few divs match for main body for', file_name

	### Grab date (includes time)
		resultDate = doc.xpath("//div[@class='dateline']")

		if len(resultDate) == 1:
			e = etree.SubElement( post_xml, "date" )
			e.text = etree.tostring( resultTitle[0], pretty_print=True)
		elif verbose:
			print 'Error: too many or too few divs match for main body for', file_name

	### Grab time (already included in date)
		resultTime = doc.xpath("//div[@class='published']")

		if len(resultTime) == 1:
			e = etree.SubElement( post_xml, "dateline" )
			e.text = etree.tostring( resultTime[0], pretty_print=True)
		elif verbose:
			print 'Error: too many or too few divs match for main body for', file_name

	### Grab tags
		resultTags = doc.xpath("//div[@class='tags']")

		if len(resultTags) == 1:
			e = etree.SubElement( post_xml, "tags" )
			e.text = etree.tostring( resultTitle[0], pretty_print=True)
		elif verbose:
			print 'Error: too many or too few divs match for main body for', file_name
		"""
	### Grab number of comments
		resultNumComments = doc.xpath("//div[@class='comments']")

		if len(resultNumComments) == 1:
			e = etree.SubElement( post_xml, "numComments" )
			e.text = etree.tostring( resultTitle[0], pretty_print=True)
		elif verbose:
			print 'Error: too many or too few divs match for main body for', file_name





	e = etree.SubElement( post_xml, "num_comments" )
	x7 = tree.xpath('//html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/div/ul/li')[0]
	e.text = etree.tostring( x7, pretty_print=True)
	print e.text
	
	"""

	except:
		if verbose: "There was an error parsing the main body for", file_name
		pass

	return post_xml


def process_livejournal_post( file_name ):
	# Create xml entry
	post_xml = etree.Element( "post" )
	
	parser = etree.HTMLParser()
	tree = etree.parse( file_name , parser)

	# Grab main body
	x1 = tree.xpath('//html/body/div/div/div/div/div/div/div/div/div/div/div/div/div')
	for x in x1:
		if 'class' in x.attrib:
			if x.attrib['class'] == 'asset-body':		
				post_xml.text = etree.tostring( x, pretty_print=True)

	###Get length
	char = str(len(post_xml.text))	
	post_xml.set( "post_char", char)
	
	### Grab title - is this an option in LJ?
	e = etree.SubElement( post_xml, "title" )
#	x2 = tree.xpath('//html/body/div/div/div/div/div/div/div/div/div/div/div/h3')[0]
#	e.text= etree.tostring( x2, pretty_print=True)

	### Grab date
	e = etree.SubElement( post_xml, "date" )
	x3 = tree.xpath('//html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/h2')
	for x in x3:
		if 'class' in x.attrib:
			if x.attrib['class'] == 'asset-name page-header2':
				e.text = etree.tostring( x, pretty_print=True)

	### Grab time
	e = etree.SubElement( post_xml, "time" )
	x4 = tree.xpath('//html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div/ul/li/span/abbr')	
	for x in x4:	
		if 'class' in x.attrib:
			if x.attrib['class'] == 'datetime':
				e.text = etree.tostring( x, pretty_print=True)

	### Grab labels (is this an option in LJ?)
	e = etree.SubElement( post_xml, "labels" )
#	x5 = tree.xpath('//html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/span')
#	for x in x5:	
#		if 'class' in x.attrib:
#			if x.attrib['class'] == 'post-labels':
#				e.text = etree.tostring( x, pretty_print=True)	

	### Grab number of comments
	e = etree.SubElement( post_xml, "num_comments" )
	x6 = tree.xpath('//html/body/div/div/div/div/div/div/div/div/div/div/div/div/ul/li/a')[0]
	e.text = etree.tostring( x6, pretty_print=True)

	return post_xml


##### Blog processors ########################################################
##############################################################################

def process_blogger_blog( file_path ):

	# Find appropriate html files
	post_files = glob.glob( file_path + '[0-9][0-9][0-9][0-9]/[0-9][0-9]/*.html' )
	return post_files
	# From the looks of it blogspot is organized in folders with yr, mo, html file

def process_wordpress_blog( file_path ):

	### Find appropriate html files
	post_files = glob.glob( file_path + '[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]/*/*.html' )
	#notes - folders with yr, mo, day, post title, then html files ("index.html" and several "index.htlm?...etc"; "index.html" is the post)

	return post_files

def process_typepad_blog( file_path ):

	### Find appropriate html files
	post_files = glob.glob( file_path + '*/[0-9][0-9][0-9][0-9]/*/*.html' )
	#notes - Folders with various names. "Files" (pdfs of uploaded docs), "photos" (jpgs of uploaded photos). The folders that have years as subfolders are the ones that contain blog posts. Archived with year, then month. For each post in the month folder there is the .html file for the post, a .html?...etc file for the post, and a folder for the post that goes to comments. This crawl just pulls the .html files in the month folder. However, this also includes an index.html file for each month, which must be deleted.

	#Remove index.html files
	good_post_files = []

	for p in post_files:
		if re.search ( 'index.html', p ) == None: good_post_files.append(p)	

	return good_post_files

def process_newsvine_blog( file_path ):

	### Find appropriate html files
	post_files = glob.glob( file_path + '*/[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]/*/*' )
	#notes about how newsvine is archived. Contains _news folder, which has posts. The subfolders for _news are years (20**). Subfolder with month, day, then html and html? files (except not listed with .html and .html? extensions).

	#Remove ? files
	good_post_files = []

	for p in post_files:
		if re.search ( '\?commentId', p ) == None and re.search ( '\?threadId', p ) == None: good_post_files.append(p)	

	return good_post_files


def process_livejournal_blog( file_path ):
	### Find appropriate html files
	post_files = glob.glob( file_path + '/[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]/*.html' )
	#notes about how livejournal is archived. Folders with year, month, day, then index.html for each post.

	return post_files

def process_unknown_blog( path, name ):
	blog_xml = etree.Element( "blog" )
	return blog_xml

##### Main dictionary ########################################################

blog_parser_dict= {
	'blogger':	process_blogger_blog,
	'wordpress': process_wordpress_blog,
	'typepad': process_typepad_blog
#	'livejournal': process_livejournal_blog,
#	'newsvine': process_newsvine_blog
}

post_parser_dict= {
	'blogger':	process_blogger_post,
	'wordpress': process_wordpress_post,
	'typepad': process_typepad_post
#	livejournal': process_livejournal_post,
#	'newsvine': process_newsvine_post
}


# API:
#	def process_[blog_type]_blog( file_path )
#		#Find html files for each of the blog posts within a blog of type blog_type stored at file_path
#		#Return a list of filenames
#
#	def process_[blog_type]_post( file_name )
#		#Parse an html blog post into xml
#		#Return xml for the blog post
#
# 	decided to put the directory syntax (/) in the input rather than the actual code
#

if __name__=="__main__":
	#Testing scripts go here:

	#files = process_newsvine_blog( '/scratch/unmirrored5/agong/blog_panel_crawl/' + 'vanessa-wilson73.newsvine.com/')
	#print len( files )
	#print files[:5]

	profiler3.testBlogParser( '/scratch/unmirrored5/agong/blog_panel_crawl/' + 'witchdoctorrepellent.blogspot.com/2005/12/no-tears-for-monster.html/'+ 
 'vanessa-wilson73.newsvine.com/', "blogger", sample=20 )


