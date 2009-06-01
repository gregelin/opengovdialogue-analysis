README - Scrape of Open Government Dialogue Brainstorm - http://opengov.ideascale.com/
Greg Elin - greg@fotonotes.net


ABOUT
=====
I wanted to get a copy of the ideas submitted to Open Government Dialogue.
Ideascale has an "alpha" API. However, the API methods only returned top 50 records. 

I downloaded the HTML of the ideas and then used Python and BeautifulSoup to scrape 
out content. The files were downloaded 5/29/09, so they should complain a set pages
complete as of the official 5/28 conclusion of the Brainstorm.


HOW TO GET HELP
===============
I'm afraid not much help available. If you encounter a problem, let me know. 
As this is a quick scrape, use caution and limit claims of accuracy.


HOW TO GET THE INFORMATION
==========================
You can get the information in various ways. 

I intend to make the GitHub Repository (#3) the primary location for this information.

1. Google Doc version: 
	http://spreadsheets.google.com/pub?key=rAFl9LChDEWCUBA8Kq9R9vw&output=html

2. Downloadable files: 
	http://gregelin.com/data/opengovdialogue-analysis

3. (Advanced) GitHub Repository 
	http://github.com/gregelin/opengovdialogue-analysis/tree
	includes downloaded html files
	includes Python scrape scripts


HOW TO WORK WITH THE FILES
==========================
The CSV version of the file is TAB-delimited. If you import the TAB-delimited version
into Excel, be sure to only have "Tab" selected as the column delimiter and not "Comma".

I left the "<br />" in to indicate line returns in the ideas themselves.

Fields are: 
	id:			XXXX-4049
	title:		Title of idea
	idea:		Text of the idea itself
	author:		Displayed name of the author
	votes:		Displayed totals votes
	votes_for:	Votes for idea (hidden in HTML)
	votes_against: Votes against idea (hidden in HTML)
	comment_count: Total number of comments
	link:		http://opengov.ideascale.com/akira/dtd/XXXX-4049  
	error:		If there is detectable error, stores that error.
	

KNOWN BAD RECORDS
=================
The following two ideas did not import very well:

http://opengov.ideascale.com/akira/dtd/2979-4049 - Appeared to be a machine-generated spam entry. Record removed.
http://opengov.ideascale.com/akira/dtd/3277-4049 - Very long record, a number of special characters. Record adjusted.


RELATED RESOURCES
=================
I also started working on python library for working with IdeaScale API.
	http://github.com/gregelin/python-ideascaleapi