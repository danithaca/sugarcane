import lxml.etree as etree


def convertToHtml(filename="temp.html"):
    blog_html = etree.Element('html')

    head_html = etree.SubElement( blog_html, 'head' )
    e = etree.Element("link", REL="StyleSheet", HREF="article_style.css", TYPE="text/css")
    head_html.append(e)

    body_html = etree.Element('body')
    for x in range(20):#blog_xml.xpath('//post'):
        body_html.append( convertPostToHtml(x) )
    blog_html.append(body_html)

    if filename:
        file(filename,'w').write( etree.tostring(blog_html, pretty_print=True) )

    return blog_html

def convertPostToHtml(x):
    doc_div = etree.Element("div")
    doc_div.set("class", "document")

    #Create the doc-header div, with all sub-divs
    doc_header = etree.Element("div")
    doc_header.set("class", "document-header")
    doc_header.text = str(x)
    doc_div.append(doc_header)

    """
    for f in ["title","author","date","labels","comment-count"]:
        try:
            e = etree.Element("div")
            e.set("class", f)
            e.text = post_xml.xpath(f)[0].text
            doc_header.append(e)
        except IndexError:
            pass
    """
#    doc_div.append(doc_header)

    doc_content = etree.Element("div")
    doc_content.set("class", "document-content")
    doc_content.text = (str(x)+" ")*20
    """
    f = etree.fromstring(post_xml.xpath('content')[0].text)
    e.append(f)
    """
    doc_div.append(doc_content)

    return doc_div
    

print etree.tostring( convertToHtml(), pretty_print=True )
