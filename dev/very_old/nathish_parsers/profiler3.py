import re, glob, csv, random, datetime
import blogsParsingNat as blogParsers
try:
	import lxml.etree as etree
except:
	import xml.etree.cElementTree as etree

def currentTime():
	return datetime.datetime.now()

### Blog-level functions #####################################################

def checkParseSuccess( xml ):
	#Checks the xml to see how complete it is
	#Returns True or False
	pass

def saveXml( file_name, xml ):
	#Saves the xml file to filename
	out_file = file( file_name, 'w' )
	out_file.write( etree.tostring( xml, pretty_print=True ) )
	out_file.close()

def predictBlogType( blog ):
	#Attempts to quickly predict blog type
	#Returns a sorted list of blog types

	#Cheating: this just returns everything, unsorted...
	return blogParsers.blog_parser_dict.keys()

def parseBlogAsType( blog, blog_type, sample=None ):
	#Attempts to parse the blog as type blog_type
	#Returns an xml tree that is as full as possible

	#Create the root xml node
	blog_xml = etree.Element( "blog" )
	blog_xml.set( "blog_name", blog )

	post_files = blogParsers.blog_parser_dict[blog_type]( '/scratch/unmirrored5/agong/blog_panel_crawl/'+blog )

	#If sample isn't None, choose the [sample] files at random to parse
	if sample:
		post_files = random.shuffle( post_files )[:sample]

	#Loop over post files
	for p in good_post_files:
		blog_xml.append( blogParsers.post_parser_dict[blog_type](p) )

	return blog_xml

def testBlogParser( blog, blog_type, sample ):
	#Attempts to parse the blog as type blog_type
	#Returns csv output reporting success
	in_path = '/scratch/unmirrored5/agong/blog_panel_crawl/'
	out_path = './xml/'

	start_time = currentTime()

	post_files = blogParsers.blog_parser_dict[blog_type]( in_path+blog+'/' )
	total_files = len( post_files )
	file_match_time_elapsed = (currentTime() - start_time)

	if total_files == 0:
		rval = [ blog, blog_type, total_files, sample, file_match_time_elapsed, 0, -1, -1, -1, -1, -1 ]
		print rval
		return rval

	#Create a root xml node
	blog_xml = etree.Element( "blog" )
	blog_xml.set( "blog_name", blog )

	#If sample isn't None, choose the [sample] files at random to parse
	random.shuffle( post_files )
	post_files = post_files[:sample]
	sample_size = len(post_files)

	has_content, has_date, has_title, has_labels, has_comments = 0, 0, 0, 0, 0
	#Loop over post files
	for p in post_files:
		xml = blogParsers.post_parser_dict[blog_type](p, verbose=False)
		if xml.text: has_content += 1
		if etree.XPath("date")(xml) and etree.XPath("date")(xml)[0].text: has_date += 1
		if etree.XPath("title")(xml) and etree.XPath("title")(xml)[0].text: has_title += 1
		if etree.XPath("labels")(xml) and etree.XPath("labels")(xml)[0].text: has_labels += 1
		if etree.XPath("comments")(xml) and etree.XPath("comments")(xml)[0].text: has_comments += 1
		blog_xml.append( xml )

	total_time_elapsed = (currentTime() - start_time)

	saveXml( out_path + blog + '-' + blog_type + '.xml', blog_xml )

	has_content = float(has_content)/sample_size
	has_date = float(has_date)/sample_size
	has_title = float(has_title)/sample_size
	has_labels = float(has_labels)/sample_size
	has_comments = float(has_comments)/sample_size

	rval = [ blog, blog_type, total_files, sample_size, file_match_time_elapsed, total_time_elapsed,
		has_content, has_date, has_title, has_labels, has_comments ]
	print rval
	return rval

	

### Main loop functions ######################################################

def parseAllBlogs():
	in_path = '/scratch/unmirrored5/agong/blog_panel_crawl/'
	out_path = '/scratch/unmirrored5/agong/blog_panel_xml/'

	#Read in a list of all the blogs
	blog_list = file('blog_list.txt','rb').read().split('\r\n')[:50][:-1]

	#Loop over the list of blogs
	for b in blog_list:
		type_list = predictBlogType( in_path+b )

		#Loop over the five most likely types
		for t in type_list[:5]:
			#Count matches
			post_files = blogParsers.blog_parser_dict[blog_type]( '/scratch/unmirrored5/agong/blog_panel_crawl/'+b )

			print len( post_files )

			#Try to parse the blog by this type
			test_xml = parseBlogAsType( b, t, sample=20 )
			if checkParseSuccess( test_xml ):
#				pass
				full_xml = parseBlogAsType( b, t )
				saveXml( out_path+b+'.xml', full_xml )



def bruteForceParseTest():
	in_path = '/scratch/unmirrored5/agong/blog_panel_crawl/'
	blog_list = file('blog_list.txt','rb').read().split('\r\n')[:-1]#[:50][:-1]

	#Create the output csv file
	my_csv = csv.writer( open('blogParsingResults.csv', 'wb') )
	my_csv.writerow( [ 'blog_url', 'blog_type', 'total_files', 'sample_size', 'file_match_time_elapsed', 'total_time_elapsed', 
		'has_content', 'has_date', 'has_title', 'has_labels', 'has_comments' ] )

	type_list = blogParsers.blog_parser_dict.keys()

	#Loop over the list of blogs and types
	for b in blog_list:
		for t in type_list:
			my_csv.writerow( testBlogParser( b, t, sample=20 ) )



if __name__=="__main__":
	bruteForceParseTest()


# API:
#	def process_[blog_type]_blog( file_path )
#		#Find html files for each of the blog posts within a blog of type blog_type stored at file_path
#		#Return a list of filenames
#
#	def process_[blog_type]_post( file_name )
#		#Parse an html blog post into xml
#		#Return xml for the blog post
#


# CSV output format
# blog - blog url
# type - the blog pattern we are attempting to match
# files_matched - number of files identified as posts
# file_match_time_elapsed - how long it took to match those files
# content
# dates_parsed
# titles_parsed
# labels
# comments




