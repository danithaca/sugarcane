import glob
import re
try:
	import lxml.etree as etree
except:
	import xml.etree.cElementTree as etree

##### Post processors ########################################################

def process_blogger_post( file_name ):
	# Create xml entry
	post_xml = etree.Element( "post" )

	parser = etree.HTMLParser()
	tree = etree.parse( file_name , parser)

	# Grab main body
	x1 = tree.xpath('//html/body/div/div/div/div/div/div/div/div/div/div/div/div')
	for x in x1:
		if 'class' in x.attrib:
			if x.attrib['class'] == 'post-body entry-content':		
				post_xml.text = etree.tostring( x, pretty_print=True)

	#Get length
	char = str(len(post_xml.text))	
	post_xml.set( "post_char", char)

	### Grab title
	e = etree.SubElement( post_xml, "title" )
	x2 = tree.xpath('//html/body/div/div/div/div/div/div/div/div/div/div/div/h3')[0]
	e.text = etree.tostring( x2, pretty_print=True)

	### Grab date
	e = etree.SubElement( post_xml, "date" )
	x3 = tree.xpath('//html/body/div/div/div/div/div/div/div/div/h2/span')[0]
	e.text = etree.tostring( x3, pretty_print=True)

	### Grab time (also grabs date and time within the xml tag <abbr>)
	e = etree.SubElement( post_xml, "time" )
	x4 = tree.xpath('//html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/span/a/abbr')	
	for x in x4:	
		if 'class' in x.attrib:
			if x.attrib['class'] == 'published':
				e.text = etree.tostring( x, pretty_print=True)

	### Grab labels
	e = etree.SubElement( post_xml, "labels" )
	x5 = tree.xpath('//html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/span')
	for x in x5:	
		if 'class' in x.attrib:
			if x.attrib['class'] == 'post-labels':
				e.text = etree.tostring( x, pretty_print=True)	

	### Grab number of comments
	e = etree.SubElement( post_xml, "num_comments" )
	x6 = tree.xpath('//html/body/div/div/div/div/div/div/div/div/div/div/div/h4')[0]
	e.text = etree.tostring( x6, pretty_print=True)

	### Grab comments
#	e = etree.SubElement( post_xml, "comments" )
#	x7 = tree.xpath('//html/body/div/div/div/div/div/div/div/div/div/div/div/div/dl/dd')
#	for x in x7:
#		if 'class' in x.attrib:
#			if x.attrib['class'] == 'comment-body':
#				print x, x.attrib

	### Get length
	e = etree.SubElement( post_xml, "length" )
	#e.text = 

	### Grab ...?


	return post_xml

def process_wordpress_post( file_name ):
	# Create xml entry
	post_xml = etree.Element( "post" )
	
	parser = etree.HTMLParser()
	tree = etree.parse( file_name , parser)

	# Grab main body (also gets some other html tags at the end (e.g. share this))
	x1 = tree.xpath('//html/body/div/div/div/div/div')
	for x in x1:
		if 'class' in x.attrib:
			if x.attrib['class'] == 'post-content':		
				post_xml.text = etree.tostring( x, pretty_print=True)

	###Get length
	char = str(len(post_xml.text))	
	post_xml.set( "post_char", char)

	### Grab title
	e = etree.SubElement( post_xml, "title" )
	x2 = tree.xpath('//html/body/div/div/div/div/h2')
	for x in x2:
		if 'class' in x.attrib:
			if x.attrib['class'] == 'post-title':
				e.text= etree.tostring( x, pretty_print=True)

	### Grab date
	e = etree.SubElement( post_xml, "date" )
	x3 = tree.xpath('//html/body/div/div/div/div/div/span')
	for x in x3:
		if 'class' in x.attrib:
			if x.attrib['class'] == 'date':
				e.text = etree.tostring( x, pretty_print=True)

	### Grab time - not an option in WP
	e = etree.SubElement( post_xml, "time" )

	### Grab categories
	e = etree.SubElement( post_xml, "categories" )
	x5 = tree.xpath('//html/body/div/div/div/div/div/div/span')
	for x in x5:	
		if 'class' in x.attrib:
			if x.attrib['class'] == 'categories':
				e.text = etree.tostring( x, pretty_print=True)

	### Grab tags
	e = etree.SubElement( post_xml, "tags" )
	x5 = tree.xpath('//html/body/div/div/div/div/div/div/span')
	for x in x5:	
		if 'class' in x.attrib:
			if x.attrib['class'] == 'tags':
				e.text = etree.tostring( x, pretty_print=True)

	### Grab number of comments
	e = etree.SubElement( post_xml, "num_comments" )
	x6 = tree.xpath('//html/body/div/div/div/div/h2')
	for x in x6:	
		if 'id' in x.attrib:
			if x.attrib['id'] == 'comments':
				e.text = etree.tostring( x, pretty_print=True)

	return post_xml

def process_typepad_post( file_name ):
	# Create xml entry
	post_xml = etree.Element( "post" )
	
	parser = etree.HTMLParser()
	tree = etree.parse( file_name , parser)

	# Grab main body
	x1 = tree.xpath('//html/body/div/div/div/div/div/div/div/div/div')
	for x in x1:
		if 'class' in x.attrib:
			if x.attrib['class'] == 'entry-body':		
				post_xml.text = etree.tostring( x, pretty_print=True)

	###Get length
	char = str(len(post_xml.text))	
	post_xml.set( "post_char", char)
	
	### Grab title
	e = etree.SubElement( post_xml, "title" )
	x2 = tree.xpath('//html/body/div/div/div/div/div/div/div/h3')
	for x in x2:
		if 'class' in x.attrib:
			if x.attrib['class'] == 'entry-header':
				e.text= etree.tostring( x, pretty_print=True)

	### Grab date
	e = etree.SubElement( post_xml, "date" )
	x3 = tree.xpath('//html/body/div/div/div/div/div/div/h2')
	for x in x3:
		if 'class' in x.attrib:
			if x.attrib['class'] == 'date-header':
				e.text = etree.tostring( x, pretty_print=True)

	### Grab time - not an option in TP
	e = etree.SubElement( post_xml, "time" )

	### Grab categories
	e = etree.SubElement( post_xml, "categories" )
	x5 = tree.xpath('//html/body/div/div/div/div/div/div/div/div/p/span')
	for x in x5:	
		if 'class' in x.attrib:
			if x.attrib['class'] == 'post-footers':
				e.text = etree.tostring( x, pretty_print=True)

	### Grab number of comments - not an option in TP
	e = etree.SubElement( post_xml, "num_comments" )

	return post_xml

def process_newsvine_post( file_name ):
	# Create xml entry
	post_xml = etree.Element( "post" )
	
	parser = etree.HTMLParser()
	tree = etree.parse( file_name , parser)

	# Grab main body
	x1 = tree.xpath('//html/body/div/div/div/div/div/div/div/div/div/div/div')
	for x in x1:
		if 'class' in x.attrib:
			if x.attrib['class'] == 'articleText':		
				post_xml.text = etree.tostring( x, pretty_print=True)

	###Get length
	char = str(len(post_xml.text))	
	post_xml.set( "post_char", char)
	
	### Grab title
	e = etree.SubElement( post_xml, "title" )
	x2 = tree.xpath('//html/body/div/div/div/div/div/div/div/div/div/div/div/h1')
	for x in x2:
		if 'class' in x.attrib:
			if x.attrib['class'] == 'gl_headline':
				e.text= etree.tostring( x, pretty_print=True)

	### Grab date (includes time)
	e = etree.SubElement( post_xml, "date" )
	x3 = tree.xpath('//html/body/div/div/div/div/div/div/div/div/div/div/div')
	for x in x3:
		if 'class' in x.attrib:
			if x.attrib['class'] == 'dateline':
				e.text = etree.tostring( x, pretty_print=True)

	### Grab time (already included in date)
	e = etree.SubElement( post_xml, "time" )
	x4 = tree.xpath('//html/body/div/div/div/div/div/div/div/div/div/div/div')
	for x in x4:
		if 'class' in x.attrib:
			if x.attrib['class'] == 'dateline':
				e.text = etree.tostring( x, pretty_print=True)

	### Grab tags
	e = etree.SubElement( post_xml, "tags" )
	x6 = tree.xpath('//html/body/div/div/div/div/div/div/div/div/div/div/div')
	for x in x6:	
		if 'class' in x.attrib:
			if x.attrib['class'] == 'tags':
				e.text = etree.tostring( x, pretty_print=True)

	### Grab number of comments
	e = etree.SubElement( post_xml, "num_comments" )
	x7 = tree.xpath('//html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/div/ul/li')[0]
	e.text = etree.tostring( x7, pretty_print=True)
	print e.text

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

def process_blogger_blog( path, name ):
	#Create root xml node and set attributes
	blog_xml = etree.Element( "blog" )
	blog_xml.set( "blog_name", name )

	# Find appropriate html files
	post_files = glob.glob( '/scratch/unmirrored5/agong/blog_panel_crawl/abusingtheprivilege.blogspot.com/20*/*/*.html' )

	#Loop over post files
	for p in post_files:
		blog_xml.append( process_blogger_post(p) )

	return blog_xml

def process_wordpress_blog( path, name ):
	#Create root xml node and set attributes
	blog_xml = etree.Element( "blog" )
	blog_xml.set( "blog_name", name )

	### Find appropriate html files
	post_files = glob.glob( '/scratch/unmirrored5/agong/blog_panel_crawl/1autolatry.wordpress.com/20*/*/*/*/*.html' )
	#notes - folders with yr, mo, day, post title, then html files ("index.html" and several "index.htlm?...etc"; "index.html" is the post)

	#Loop over post files
	for p in post_files:
		text = file(p, 'r').read()
		blog_xml.append( process_wordpress_post(p) )

	return blog_xml

def process_typepad_blog( path, name ):
	#Create root xml node and set attributes
	blog_xml = etree.Element( "blog" )
	blog_xml.set( "blog_name", name )

	### Find appropriate html files
	post_files = glob.glob( '/scratch/unmirrored5/agong/blog_panel_crawl/advocatefornurses.typepad.com/*/20*/*/*.html' )
	#notes - Folders with various names. "Files" (pdfs of uploaded docs), "photos" (jpgs of uploaded photos). The folders that have years as subfolders are the ones that contain blog posts. Archived with year, then month. For each post in the month folder there is the .html file for the post, a .html?...etc file for the post, and a folder for the post that goes to comments. This crawl just pulls the .html files in the month folder. However, this also includes an index.html file for each month, which must be deleted.

	#Remove index.html files
	good_post_files = []

	for p in post_files:
		if re.search ( 'index.html', p ) == None: good_post_files.append(p)	

	#Loop over good post files
	for p in good_post_files:
		text = file(p, 'r').read()
		blog_xml.append( process_typepad_post(p) )

	return blog_xml

def process_newsvine_blog( path, name ):
	#Create root xml node and set attributes
	blog_xml = etree.Element( "blog" )
	blog_xml.set( "blog_name", name )

	### Find appropriate html files
	post_files = glob.glob( '/scratch/unmirrored5/agong/blog_panel_crawl/amircarr2000.newsvine.com/*/20*/*/*/*' )
	#notes about how newsvine is archived. Contains _news folder, which has posts. The subfolders for _news are years (20**). Subfolder with month, day, then html and html? files (except not listed with .html and .html? extensions).

	#Remove ? files
	good_post_files = []

	for p in post_files:
		if re.search ( '\?commentId', p ) == None and re.search ( '\?threadId', p ) == None: good_post_files.append(p)	

	#Loop over post files
	for p in good_post_files:
		text = file(p, 'r').read()
		blog_xml.append( process_newsvine_post(p) )

	return blog_xml

def process_livejournal_blog( file_path ):
	### Find appropriate html files
	post_files = glob.glob( file_path + '/20[0-9][0-9]/*/*/*.html' )
	#notes about how livejournal is archived. Folders with year, month, day, then index.html for each post.

	return post_files

def process_unknown_blog( path, name ):
	blog_xml = etree.Element( "blog" )
	return blog_xml

##### Main dictionary ########################################################

blog_parser_dict= {
	'blogger':	process_blogger_blog,
	'wordpress': process_wordpress_blog,
	'typepad': process_typepad_blog,
	'livejournal': process_livejournal_blog,
	'newsvine': process_newsvine_blog
}

post_parser_dict= {
	'blogger':	process_blogger_post,
	'wordpress': process_wordpress_post,
	'typepad': process_typepad_post,
	'livejournal': process_livejournal_post,
	'newsvine': process_newsvine_post
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

if __name__=="__main__":
	#Testing scripts go here:

	files = process_livejournal_blog( '/scratch/unmirrored5/agong/blog_panel_crawl/' + 'alas-a-llama.livejournal.com' )
	print len( files )
	print files[:5]




