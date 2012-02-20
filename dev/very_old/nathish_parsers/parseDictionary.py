import glob
import re
try:
	import lxml.etree as etree
except:
	import xml.etree.cElementTree as etree

blog_parser_dict = {
	'blogger': process_blogger_blog
	'wordpress': process_wordpress_blog
	'typepad': process_typepad_blog
	'livejournal': process_livejournal_blog
	'newsvine': process_newsvine_blog}


