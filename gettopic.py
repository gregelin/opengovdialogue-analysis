#!/usr/bin/python
"""A script to parse Open Gov Dialogue

   Changes:
   05.31.2009: Created IdeaScaleScrapeExtractor Class
"""

__author__="Greg Elin"
__version__="$Revision: 0.1$"
__date__="$Date: 2009/05/30"
__copyright__="(CC) By Attribution"
__license__="Python"

# TODO:
# TODO - why is the following line removing \r and other items? Too greedy?
#'<(?!\/?a(?=>|\s.*>))\/?.*?>' : ' ',

# Imports
from BeautifulSoup import BeautifulSoup
import urllib2
import re
import datetime
import glob

# Config
testfile="data/2468-4049"
testfile2="data/2430-4049"
scrape_date=datetime.datetime(2009,05,28)

# Utilities
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

# Extractor Class

class IdeaScaleScrapeExtractor(object):
    """Extract various content from a scrape of IdeaScale Idea page"""
    
    def __init__(self, file=None, scrape_date=datetime.datetime(2009,05,28)):
        super(IdeaScaleScrapeExtractor, self).__init__()
        self.file=file
        self.scrape_date=scrape_date
        
        self.id=None
        self.relative_age=None
        self.created=None
        self.author=None
        self.comment_count=None
        self.title=None
        self.ideas=None
        self.votes=None
        
        try:
            self.soup=BeautifulSoup(open(self.file))
            self.set_id()
            self.set_link()
            self.set_valid()
            if self.valid==True:
                self.set_relative_age()
                self.set_created()
                self.set_author()
                self.set_comment_count()
                self.set_title()
                self.set_idea()
                self.set_votes()
        except Exception, e:
            raise e

    def set_valid(self):
        # Determine if file is an idea or invalid link
        self.valid=False
        if self.soup.find(text=re.compile("The link you have clicked is invalid."))==None:
            self.valid=True
        
    def set_relative_age(self):
        # start IdeaScale_IdeaSubTitle
        try:
            self.relative_age=self.soup.find('div', id=re.compile('IdeaScale_IdeaSubTitle')).contents[0].nextSibling.nextSibling.contents[0]
        except Exception, e:
            raise e
        
    def set_created(self):
        hd=re.search("hour|day",self.relative_age).group()
        self.created=hd
        val=int(re.search("[0-9]+",self.relative_age).group())
        self.created=val
        self.created=self.scrape_date
        if hd=="day":
            self.created=self.scrape_date - datetime.timedelta(days=val)
        
    def set_author(self):
        # start IdeaScale_IdeaSubTitle
        self.author=self.soup.find('div', id=re.compile('IdeaScale_IdeaSubTitle')).contents[0].contents[0].contents[0]
        #self.author=text_soup.contents[0].contents[0].contents[0]

    def set_comment_count(self):
        # start FlagComment
        self.comment_count=len(self.soup.findAll('span', id=re.compile('FlagComment')))
        
    def set_link(self):
        self.link="http://opengov.ideascale.com/akira/dtd/%s" % self.id

    def set_title(self):
        # start IdeaScale_IdeaTitle
        self.title=self.soup.find('div', id=re.compile('IdeaScale_IdeaTitle')).contents[0]

    def set_id(self):
        self.id=re.search("[0-9]+-4049",self.file).group()
    
    def set_idea(self):
        # Start at find(id="DiscussionTopicText_2426").contents[2]
        # End at <h3>Why Is This Idea Important?</h3>
        text_soup=self.soup.find('div', id=re.compile('DiscussionTopicText_'))
        idea="".join(["%s" % text for text in text_soup.contents[2:]])
        idea=clean_line_endings(clean_utf8(idea))
        self.idea=re.sub(r'^(<br /><br /><br /><br /><br />)(.*)',r'\2',idea,1).strip()
    
    def set_votes(self):
        # Start at <div id="IdeaScale_Vote" 
        self.fvor=0
        self.vagainst=0
        text_soup=self.soup.find('div',id=re.compile('IdeaScale_Vote'))
        self.vfor=int(re.search("[0-9]+",text_soup.contents[1].contents[0].contents[1].contents[0]).group()) # votes for
        self.vagainst=int(re.search("[0-9]+",text_soup.contents[1].contents[0].contents[2].contents[0]).group()) # votes against
        self.vtotal=self.vfor-self.vagainst

# Main

def main():
    files=glob.glob('data/*-4049')
    print "id\ttitle\tcreated\tidea\tauthor\tvotes\tvotes_for\tvotes_against\tcomment_count\tlink"
    
    for file in files[1100:1120]:
        myIdea=IdeaScaleScrapeExtractor(file,scrape_date)
        if myIdea.valid==True:
            try:
                #myIdea=IdeaScaleScrapeExtractor()
                #myIdea.soup=BeautifulSoup(open(file))
                #print myIdea.file
                #print myIdea.soup
                #print "id: %s" % myIdea.id
                #print "author: %s" % myIdea.author
                #print "relative_age: %s" % myIdea.relative_age
                #print "created: %s" % myIdea.created
                #print "comment_count: %s" % myIdea.comment_count
                #print "idea: %s" % myIdea.idea
                #print "vfor: %d vagainst: %d vtotal: %d" % (myIdea.vfor, myIdea.vagainst, myIdea.vtotal)
                #print myIdea.soup
                #idea=myIdea.get_topic(soup)
                #link = "http://opengov.ideascale.com/akira/dtd/%s" % id

                print "%s\t%s\t%s\t%s\t%s\t%d\t%d\t%d\t%d\t%s" % (myIdea.id,myIdea.title,myIdea.created,myIdea.idea,myIdea.author.strip(),myIdea.vtotal,myIdea.vfor,myIdea.vagainst,myIdea.comment_count,myIdea.link)
            except Exception, e:
                raise e


if __name__ == '__main__':
    main()