#!/usr/bin/python
"""A library to quickly scrape web pages.
   

"""

__author__ = "Greg Elin (greg@fotonotes.net)"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2009/05/29 $"
__copyright__ = "(CC) By Attribution"
__license__ = "Python"

# TODO:

# Imports
from BeautifulSoup import BeautifulSoup
import urllib2
import re
import datetime

def main():
    # url template
    url_template='http://opengov.ideascale.com/akira/dtd/%s-4049'
    
    for id in range(2420,3930):
        url=url_template % id
        try:
            print "downloading %s" % url
            r=urllib2.urlopen(url).read()
        except:
            r=None
        
        file_template='data/%s-4049'
        target_file=file_template % id
        try:
            f=open(target_file,"w")
            f.write(r)
            f.close()
            print "saved %s" % target_file
        except:
            print "Unable to save file %s" % target_file


if __name__=="__main__":
    main()
    