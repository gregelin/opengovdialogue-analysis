#!/usr/bin/python
"""A script to parse Open Gov Dialogue

"""

__author__="Greg Elin"
__version__="$Revision: 0.1$"
__date__="$Date: 2009/05/30"
__copyright__="(CC) By Attribution"
__license__="Python"

# TODO:
# TODO - why is the following line removing \r and other items? Too greedy?
#'<(?!\/?a(?=>|\s.*>))\/?.*?>' : ' ',

# Config
testfile="data/2468-4049"
testfile2="data/2430-4049"

# Imports
from BeautifulSoup import BeautifulSoup
import urllib2
import re
import datetime
import glob

def clean(text):
    try:
        text = text.replace("&nbsp; ","")
    except:
        pass    
    text = text.strip()
    
    return text
    
def clean_utf8(text):
    text = text.decode("utf-8")
    text = text.replace(u"\u201c", "\"").replace(u"\u201d", "\"") 
    text = text.replace(u"\u2018", "'").replace(u"\u2019", "'") 
    # trademark, short dash, long dash
    text = text.replace(u"\u2122", "(tm)").replace(u"\u2013", "-").replace(u"\u2014", "--")
    
    return text
    
def clean_line_endings(text):
    patterns = {# turn indicated paragraphs into new lines
        '</?p>' : "\r\n",
        '<p class="MsoBodyTextIndent">' : "\r",
        "<p .*?>" : "\r\n",
        # turn line breaks into returns
        #'</?br ?/?>' : "\r\n",
        # turn fixed spaces into single space
        '&nbsp;' : " ",
        # isolate any headings on their own line
        '</?h[1234568]>' : "\r\n",
        # Fix weird large blocks. Example:
        '&lt;!--\r\r([ ./\w\W]*?)--&gt;' : "\r",
        # make <li> into new lines
        '<li>|<li .*?>[ ]*' :  "\r    -",
        '</li>' : " ",
        # make <ul> into new lines
        '<ul>|<ul .*?>[ ]*' : "\r/*ed: unordered list*/",
        '<ol>|<ol .*?>[ ]*' : "\r/*ed: ordered list*/",
        # remove all remaining HTML tags except for links
        # TODO - why is the following line removing \r and other items? Too greedy?
        #'<(?!\/?a(?=>|\s.*>))\/?.*?>' : ' ',
        # clean up blank lines
        #'[ ]+\n' : "\n",
        #'[\t]+\n' : "\n",
        # convert three or more returns to two returns
        #'\r\r\r*' : "\r\r",
        # convert three or more returns to two returns
        #'\n\n\n*' : "\r\r",
        # convert two or more spaces to two spaces
        "[ ]+" : ' ',
        # convert tabs to spaces
        "\t" : '    ',
        #'[ ]+\n\n' : "\n\n",
        '[ ]+\n\n' : "<br /><br />",
        "\n|\r" : "<br />",
        #'[\t]+\n' : "\r",
         # convert three or more returns to two returns
         '\r\r\r*' : "\r\r",
          "\r\r": "<br /><br /><br />"
         
     }
    
    for key in patterns.keys():
        text = re.sub(key,patterns[key],text)
    return text

def get_topic(soup):
    # Start at find(id="DiscussionTopicText_2426").contents[2]
    # End at <h3>Why Is This Idea Important?</h3>
    text_soup=soup.find('div', id=re.compile('DiscussionTopicText_'))
    r="".join(["%s" % text for text in text_soup.contents[2:]])
    r=clean_line_endings(clean_utf8(r))
    return r
    
def get_votes(soup):
    # Start at <div id="IdeaScale_Vote" 
    r="0"
    text_soup=soup.find('div',id=re.compile('IdeaScale_Vote'))
    #return text_soup
    vfor=int(re.search("[0-9]+",text_soup.contents[1].contents[0].contents[1].contents[0]).group()) # votes for
    vagainst=int(re.search("[0-9]+",text_soup.contents[1].contents[0].contents[2].contents[0]).group()) # votes against
    vtotal=vfor-vagainst
    return vfor,vagainst,vtotal
    
def get_author(soup):
    """
    IdeaScale_IdeaSubTitle
    
    """
    text_soup=soup.find('div', id=re.compile('IdeaScale_IdeaSubTitle'))
    a=text_soup.contents[0].contents[0].contents[0]
    return a
    
def get_comment_count(soup):
    text_soup=soup.findAll('span', id=re.compile('FlagComment'))
    cnt=len(text_soup)
    return cnt
    
def get_idea_title(soup):
    # start IdeaScale_IdeaTitle
    text_soup=soup.find('div', id=re.compile('IdeaScale_IdeaTitle'))
    t=text_soup.contents[0]
    return t
    
    
def main():
    files=glob.glob('data/*-4049')
    #print "<table>"
    #print """<tr>
    #<td>id</td>
    #<td>link</td>
    #<td>title</td>
    #<td>author</td>
    #<td>votes</td>
    #<td>votes_for</td>
    #<td>votes_against</td>
    #<td>idea</td>
    #</tr>
    #"""
    print "id\ttitle\tidea\tauthor\tvotes\tvotes_for\tvotes_against\tcomment_count\tlink"
    
    for file in files:
        id=re.search("[0-9]+-4049",file).group()
        try:
            soup=BeautifulSoup(open(file))
            title=get_idea_title(soup)
            idea=get_topic(soup)
            vfor,vagainst,vtotal=get_votes(soup)
            author=get_author(soup)
            cnt=get_comment_count(soup)
            link = "http://opengov.ideascale.com/akira/dtd/%s" % id
            print "%s\t%s\t%s\t%s\t%d\t%d\t%d\t%d\t%s" % (id,title,re.sub(r'^(<br /><br /><br /><br /><br />)(.*)',r'\2',idea,1).strip(),author.strip(),vtotal,vfor,vagainst,cnt,link)
            
            #print "<tr>"
            #print "<td class='id'>%s</td>" % id
            #print "<td class='link'>http://opengov.ideascale.com/akira/dtd/%s</td>" % id
            #print "<td class='title'>%s</td>" % title
            #print "<td class='author'>%s</td>" % author
            #print "<td class='votes'>%d</td>" % vtotal
            #print "<td class='votes_for'>%d</td>" % vfor
            #print "<td class='votes_against'>%d</td>" % vagainst
            #print "<td class='idea'>%s</td>" % idea.strip()
            #print "</tr>"
        except:
            pass
            #print "Problem with file %s" % file
    #print "</table>"
        
if __name__ == '__main__':
    main()